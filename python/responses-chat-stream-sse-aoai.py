from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    api_key = os.environ["AZURE_OPENAI_API_KEY"],  
    api_version = os.environ["AZURE_OPENAI_API_VERSION"],
    azure_endpoint = os.environ["AZURE_OPENAI_API_ENDPOINT"]
    )

previous_response_id = None

while True:
    user_input = input("Enter your message (or type 'exit' to quit): ").strip()
    if user_input.lower() == "exit":
        break

    params = {
        "model": os.environ["AZURE_OPENAI_API_MODEL"],
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