# Importing required packages
from openai import AzureOpenAI
import os
# Setting up Azure OpenAI client with the necessary credentials
model_name = "gpt-5"
deployment = "gpt-5"
endpoint = os.environ.get("AOAI_ENDPOINT", "UNKNOWN_AOAI")
subscription_key = os.environ.get("AOAI_APIKEY", "UNKNOWN_AOAI_APIKEY")
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

class GPT:
    @staticmethod
    def code_completion(user_content):
        chat_completion = client.chat.completions.create(
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
            model=deployment,
            max_completion_tokens=16384,
        )
        return chat_completion
