import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_V1_API_ENDPOINT"),
)

response = client.responses.create(
    model=os.environ["AZURE_OPENAI_API_MODEL"],
    input="Tell me a joke.",
    service_tier="priority"
)

print(response.output_text)
print("Service Tier:", response.service_tier)