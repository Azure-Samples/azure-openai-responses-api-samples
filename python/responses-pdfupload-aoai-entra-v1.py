from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import os
from dotenv import load_dotenv
from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)

load_dotenv()

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = get_azure_openai_v1_base_url(),  
  api_key = token_provider
)

# Upload a file with a purpose of "batch"
file = client.files.create(
  file=open("../assets/employee_handbook.pdf", "rb"), # This assumes a .pdf file in the assets directory
  purpose="assistants"
)

response = client.responses.create(
    model=get_azure_openai_deployment_name(),
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_id":file.id
                },
                {
                    "type": "input_text",
                    "text": "What are the company values?",
                },
            ],
        },
    ]
)

print(response.output_text)