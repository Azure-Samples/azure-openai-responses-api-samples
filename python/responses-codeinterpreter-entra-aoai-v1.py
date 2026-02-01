from openai import OpenAI 
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)

import os
load_dotenv()

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = get_azure_openai_v1_base_url(),  
  api_key = token_provider
)

instructions = "You are a personal math tutor. When asked a math question, write and run code using the python tool to answer the question."

response = client.responses.create(
    model = get_azure_openai_deployment_name(), 
    tools = [
        {
            "type": "code_interpreter",
            "container": {"type": "auto"}
        }
    ],
    instructions=instructions,
    input="I need to solve the equation 3x + 11 = 14. Can you help me?",
)

print(response.output_text)