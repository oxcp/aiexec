import asyncio
import os
import sys
import importlib.util
from copilot import CopilotClient

# Load the skill module dynamically
skill_path = os.path.join(os.getcwd(), ".copilot_skills", "pr_skills", "pr_tools.py")
spec = importlib.util.spec_from_file_location("pr_tools", skill_path)
pr_tools = importlib.util.module_from_spec(spec)
sys.modules["pr_tools"] = pr_tools
spec.loader.exec_module(pr_tools)

get_pr_details = pr_tools.get_pr_details
list_prs = pr_tools.list_prs

async def approve_all(request):
    return {"kind": "approved"}

async def main():
    repo = "kylercai/javademo"
    print(f"Analyzing all PRs for {repo} using Copilot Skills...")
    
    # Initialize the Copilot client
    client = CopilotClient()
    await client.start()

    try:
        # Create a session with the skill
        print("Starting Copilot session...")
        session = await client.create_session({
            "model": "claude-sonnet-4.5",
            "streaming": True,
            "tools": [list_prs, get_pr_details],
            "on_permission_request": approve_all
        })

        # Send the prompt asking Copilot to use the skill
        prompt = f"""
Please analyze ALL pull requests in the repository '{repo}'.

1. Use the `list_prs` tool to get a list of all PRs (open, closed, merged).
2. For EACH PR in the list, use `get_pr_details` to fetch its full details (body, changes, etc.).
3. Provide a comprehensive summary for every PR.

Do not skip any PR.
"""
        print("Sending prompt to Copilot...")
        response = await session.send_and_wait({
            "prompt": prompt
        }, timeout=600)  # Increased timeout for multiple tool calls

        # Print the response content
        print("\nAnalysis Result:")
        print("-" * 40)
        print(response.data.content)
        print("-" * 40)

        # Clean up
        await session.destroy()
    
    finally:
        await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
