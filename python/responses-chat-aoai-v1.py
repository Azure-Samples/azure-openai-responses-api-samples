import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_V1_API_ENDPOINT"),
)

previous_response_id = None

while True:
    user_input = input("Enter your message (or type 'exit' to quit): ").strip()
    if user_input.lower() == "exit":
        break

    params = {
        "model": os.environ["AZURE_OPENAI_API_MODEL"],
        "input": [{"role": "user", "content": user_input}]
    }
    
    if previous_response_id:
        params["previous_response_id"] = previous_response_id
    
    response = client.responses.create(**params)

    print(response.output_text)
    previous_response_id = response.id