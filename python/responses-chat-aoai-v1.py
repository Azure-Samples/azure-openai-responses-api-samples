from os import environ
from dotenv import load_dotenv
from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)

from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=environ["AZURE_OPENAI_API_KEY"],
    base_url=environ["AZURE_OPENAI_V1_API_ENDPOINT"],
)
model, prev_id = environ["AZURE_OPENAI_API_MODEL"], None

while (msg := input("Enter your message ('exit' to quit): ").strip()).lower() != "exit":
    response = client.responses.create(
        model=model,
        input=[{"role": "user", "content": msg}],
        **({"previous_response_id": prev_id} if prev_id else {}),
    )
    print(response.output_text)
    prev_id = response.id