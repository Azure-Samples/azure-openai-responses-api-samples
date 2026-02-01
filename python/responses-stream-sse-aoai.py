# Uses Server Side Events (SSE) to stream the response one line at a time
from openai import AzureOpenAI
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

client = AzureOpenAI(
    api_key = get_azure_openai_api_key(),  
    api_version = get_azure_openai_api_version(),
    azure_endpoint = get_azure_openai_endpoint()
    )

stream = client.responses.create(
    model= get_azure_openai_deployment_name(),
    input="Write me a poem about the sea.",
    stream=True,
)

for event in stream:
    if event.type == 'response.output_text.delta':
        print(event.delta, end='')