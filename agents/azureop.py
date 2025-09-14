from asyncio import subprocess
import json
import os
import subprocess
import time
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool
from azure.ai.agents.models import FunctionTool

#--- Define user functions ---
def save_script(script: str) -> str:
    """
    Saves the provided script to a file.

    :param script: The script to save.
    :return: Confirmation message with the file name.
    """
    try:
        filename = "./generated_script.sh"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(script)

        # get the absolute path and filename of the saved script
        filepath = os.path.abspath(filename)
        print(f"Script saved to {filepath}")
        return filepath
    except Exception as e:
        print(f"Error saving script: {str(e)}")
        return f"Error saving script: {str(e)}"

def run_script(script: str) -> str:
    """
    Run the provided script.

    :param script: The script to save and execute.
    :return: The output of the script execution.
    """
    try:
        filepath = save_script(script)
        # execute the bash shell script, wait until it finishes and print the output
        print(f"Executing script: {filepath}")
        result = subprocess.run(["bash", filepath], capture_output=True, text=True)
        print(result.stdout)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error saving or executing script: {str(e)}"
    
#--- End of defining user functions ---


# Define user functions
user_functions = {save_script, run_script}
# Initialize the FunctionTool with user-defined functions
functions = FunctionTool(functions=user_functions)
#code_interpreter = CodeInterpreterTool()

# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.getenv("PROJECT_ENDPOINT","https://kacai-3055-resource.services.ai.azure.com/api/projects/kacai-3055")  # Ensure the PROJECT_ENDPOINT environment variable is set
# # Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
)

sysprompt = """
You are an Azure operation assistant helping people to automatically perform resources management and application deployment. Generate necessary scripts or code and run it as needed. Please follow:
1. if the script interacts with Azure, use Azure CLI
2. if the script needs to login to azure, use service principal without human interaction.
3. if save the script to a file, or run the script, convert the script to bash shell first
4. if you need any input from people, just ask for the input
"""

useexistingagent = False
with project_client:
    if not useexistingagent:
        # create an agent with code interpreter tool
        agent = project_client.agents.create_agent(
            #model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
            model="gpt-4o",  # Specify the model to use
            name="AzureOpAgent",  # Name of the agent
            instructions=sysprompt,  # Instructions for the agent
            tools=functions.definitions,  # Attach the tools
        )
        print(f"Created agent, ID: {agent.id}")
    else:
        # retrieve the existing agent
        agent = project_client.agents.get_agent("<your_existing_agent_id, e.g. asst_bfsxMq7rr7xoxHqE4rNfq9oG>")
        print(f"Retrieved agent, ID: {agent.id}")

    try:
        # Create a thread for communication
        thread = project_client.agents.threads.create()
        print(f"Created thread, ID: {thread.id}")
        
        userprompt = ""
        print("------\nUser:")
        while True:
            line = input("")
            userprompt += line  # Continue to build the prompt
            if line.endswith("\\"):
                continue

            if userprompt:
                # if the inputprompt is "exit", then break the loop
                if userprompt.lower() == "exit":
                    break

                # Add a message to the thread
                project_client.agents.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=userprompt
                )

                # Create and process an agent run
                #run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
                run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)

                # Poll until run completes
                while run.status in ["queued", "in_progress", "requires_action"]:
                    time.sleep(1)
                    run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

                    if run.status == "requires_action":
                        tool_calls = run.required_action.submit_tool_outputs.tool_calls
                        tool_outputs = []
                        for tool_call in tool_calls:
                            if tool_call.function.name == "save_script":
                                #print(f"Saving script: {tool_call.function.arguments}")
                                # save the script to a file
                                output = save_script(json.loads(tool_call.function.arguments).get('script', ''))
                                tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
                            if tool_call.function.name == "run_script":
                                #print(f"Running script: {tool_call.function.arguments}")
                                # run the script value and get the output
                                output = run_script(json.loads(tool_call.function.arguments).get('script', ''))
                                tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
                        project_client.agents.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)

                if run.status == "failed":
                    print(f"Run failed: {run.last_error}")
                    break  # Skip fetching user prompt if the run failed

                # Fetch and log all messages
                # messages = project_client.agents.messages.list(thread_id=thread.id)
                # # print the last message in messages

                response = project_client.agents.messages.get_last_message_text_by_role(thread.id, "assistant")
                print(f"Assistant: {response.text.value}")

                userprompt = ""
                print("------\nUser:")
    except Exception as e:
        print(f"Error during agent run: {str(e)}")
    finally:
        if not useexistingagent:
            # if we create a new agent for above task, delete the agent when done
            project_client.agents.delete_agent(agent.id)
            print("Deleted agent")