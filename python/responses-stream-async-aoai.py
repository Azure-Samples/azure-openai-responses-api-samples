# Uses async client to continuously stream data from the server to the client.
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)

import os
import asyncio

load_dotenv()

client = AsyncAzureOpenAI(
    api_key = get_azure_openai_api_key(),  
    api_version = get_azure_openai_api_version(),
    azure_endpoint = get_azure_openai_endpoint()
    )

async def main():
    stream = await client.responses.create(
        model=get_azure_openai_deployment_name(),
        input="Write me a poem about the sea.",
        stream=True,
    )

    async for event in stream:
        if hasattr(event, "delta") and event.delta:
            print(event.delta, end="", flush=True)

asyncio.run(main())