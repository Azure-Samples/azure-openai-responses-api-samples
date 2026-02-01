# Uses async client to continuously stream data from the server to the client.
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)

import asyncio

load_dotenv()

client = AsyncOpenAI(
    api_key=get_azure_openai_api_key(),
    base_url=get_azure_openai_v1_base_url(),

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