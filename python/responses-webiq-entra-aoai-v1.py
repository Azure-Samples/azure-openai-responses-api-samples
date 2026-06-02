import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

webiq_api_key = os.getenv("WEBIQ_API_KEY")

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = os.getenv("AZURE_OPENAI_V1_API_ENDPOINT"),  
  api_key = token_provider
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
