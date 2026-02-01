import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)


load_dotenv()

client = AzureOpenAI(
    api_key = get_azure_openai_api_key(),  
    api_version = get_azure_openai_api_version(),
    azure_endpoint = get_azure_openai_endpoint()
    )

response = client.responses.create(
    model=get_azure_openai_deployment_name(),
    input="Tell me a joke."

)

print(response.output_text)