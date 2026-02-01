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
        "input": [{"role": "user", "content": user_input}],
        "stream": True
    }
    
    if previous_response_id:
        params["previous_response_id"] = previous_response_id

    stream = client.responses.create(**params)

    for event in stream:
        # Check for the event type that contains the response ID
        if event.type == 'response.created':
            previous_response_id = event.response.id

        # Process the event output
        if event.type == 'response.output_text.delta':
            print(event.delta, end='')

    print()  # Newline after processing stream output