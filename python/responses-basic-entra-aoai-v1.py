import os
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


load_dotenv()

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = get_azure_openai_v1_base_url(),  
  api_key = token_provider
)

response = client.responses.create(
    model=get_azure_openai_deployment_name(),
    input="Tell me a joke."

)

print(response.output_text)
