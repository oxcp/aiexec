from prompts import Prompt
import os
import json
import time
from gpt import GPT
from aigateway import AIGateway
import sys
from loadConfigure import VerifyConfiguration

class Verifier:
    @staticmethod
    def verify_with_prompt_file(model: str, prompt_file: str) -> str:
        parsed_prompts = Prompt.parse_structured_prompts_file(prompt_file)
        for prompt in parsed_prompts:
            prompt_json = json.dumps(prompt)
            #print(f"Verifying prompt: \n{json.loads(prompt_json).get('prompt')}\n")
            print(f"\n***************** Verifying model: {model} *****************\n")
            starttime = time.time()

            if (model == "gpt5"):
                completion = GPT.code_completion(json.loads(prompt_json).get("prompt"))
            else:
                ai_gateway = AIGateway(model)
                completion = ai_gateway.get_completion(json.loads(prompt_json).get("prompt"))

            duration = round(time.time() - starttime, 3)
            return f"Duration: {duration} seconds.\nOutput:\n{completion.choices[0].message.content}"

    def save_output_to_file(output: str, file_path: str) -> None:
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(output)

#code for main
if __name__ == "__main__":
    vc = VerifyConfiguration()
    models_json = vc.models_json
    scenarios_json = vc.scenarios_json    

    # for each model in the models_json
    for model in json.loads(models_json):
        print(f"\n***************** Verifying model: {model} *****************")
        # for each scenario in the scenarios_json
        for scenario in json.loads(scenarios_json):
            prompt_file = f"prompts-{scenario}.yaml"
            output_file = f"response-{model}-{scenario}.txt"
            print(f"prompt_file={prompt_file} output_file={output_file}")
            output_file_content = Verifier.verify_with_prompt_file(model, prompt_file)
            #print(f"Output for {model}:\n\n{output_file_content}")
            Verifier.save_output_to_file(output_file_content, output_file)
            print(f"Output saved to {output_file}\n")

    # if len(sys.argv) < 3:
    #     print("Usage: python verifier.py <model> <prompt_file> <output_file(optional)>")
    #     sys.exit(1)
    # model = sys.argv[1]
    # prompt_file = sys.argv[2]
    # completion_content = Verifier.verify_with_prompt_file(model, prompt_file)
    # print(f"Code generated:\n{completion_content}")
    # if len(sys.argv) == 4:
    #     output_file = sys.argv[3]
    #     Verifier.save_output_to_file(completion_content, output_file)
    #     print(f"Output saved to {output_file}")