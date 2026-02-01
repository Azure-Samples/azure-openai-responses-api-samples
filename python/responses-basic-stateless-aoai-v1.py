import os
from openai import OpenAI
from dotenv import load_dotenv
from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)


load_dotenv()

client = OpenAI(
    api_key=get_azure_openai_api_key(),
    base_url=get_azure_openai_v1_base_url(),
)

response = client.responses.create(
    model=get_azure_openai_deployment_name(),
    input="Tell me a joke.",
    store=False, #store=false, to avoid storing sensitive data
    include=["reasoning.encrypted_content"] # Encrypted chain of thought is passed back in the response
)

print(response.output_text)