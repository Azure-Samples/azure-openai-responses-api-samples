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
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "Describe this image" },
                {
                    "type": "input_image",
                    "image_url": "https://learn.microsoft.com/azure/well-architected/ai/images/responsible-ai.png"
                }
            ]
        }
    ]
)

print(response.output_text)
