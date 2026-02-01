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

previous_response_id = None

while True:
    user_input = input("Enter your message (or type 'exit' to quit): ").strip()
    if user_input.lower() == "exit":
        break

    params = {
        "model": get_azure_openai_deployment_name(),
        "input": [{"role": "user", "content": user_input}]
    }
    
    if previous_response_id:
        params["previous_response_id"] = previous_response_id
    
    response = client.responses.create(**params)

    print(response.output_text)
    previous_response_id = response.id