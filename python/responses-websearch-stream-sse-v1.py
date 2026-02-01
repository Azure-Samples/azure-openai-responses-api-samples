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
    base_url=get_azure_openai_v1_base_url()
)

stream = client.responses.create(
    model= get_azure_openai_deployment_name(),
    tools=[{"type": "web_search_preview"}],
    input="Give me a positive news story from the web today",
    stream=True,
)

for event in stream:
    if event.type == 'response.output_text.delta':
        print(event.delta, end='')