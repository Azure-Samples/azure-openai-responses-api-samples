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

from time import sleep

load_dotenv()

client = OpenAI(
    api_key=get_azure_openai_api_key(),
    base_url=get_azure_openai_v1_base_url(),
)

response = client.responses.create(
    model = "o3-pro",
    input = "Write me a very long story",
    background = True
)

while response.status in {"queued", "in_progress"}:
    print(f"Current status: {response.status}")
    sleep(2)
    response = client.responses.retrieve(response.id)

print(f"Final status: {response.status}\nOutput:\n{response.output_text}")
