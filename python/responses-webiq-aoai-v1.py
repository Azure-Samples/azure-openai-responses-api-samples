import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

webiq_api_key = os.getenv("WEBIQ_API_KEY")

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_V1_API_ENDPOINT"),
)

response = client.responses.create(
    model=os.environ["AZURE_OPENAI_API_MODEL"],
    tools=[
        {
            "type": "mcp",
            "server_label": "WebIQ",
            "server_url": "https://api.microsoft.ai/v3/mcp",
            "require_approval": "never",
            "headers": {"x-apikey": webiq_api_key},

        },
    ],
    input="What is the latest image-gen model from MAI?",
)

print(response.output_text)
