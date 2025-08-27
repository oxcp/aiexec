from openai import OpenAI
import os

class AIGateway:
    endpoint = os.environ.get("AIGW_ENDPOINT", "UNKNOWN_AIGW")
    api_key = os.environ.get("AIGW_APIKEY", "UNKNOWN_AIGW_APIKEY")

    def __init__(self, model_name):
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.api_key,
        )
        self.model_name = model_name

    def get_completion(self, user_content):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that helps people resolve coding and bug fixing tasks in development.",
                },
                {
                    "role": "user",
                    "content": user_content,
                }
            ],
            max_tokens=16384,
        )
        return response

# Example usage:
# model_name = "claude-opus-4-1-20250805"
# #model_name = "claude-opus-4-1-20250805-thinking"
# ai_gateway = AIGateway(model_name)
# response = ai_gateway.get_completion("Hello")
# print(response.choices[0].message.content)