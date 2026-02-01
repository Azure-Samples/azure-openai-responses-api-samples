import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)


load_dotenv()

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = get_azure_openai_v1_base_url(),  
  api_key = token_provider
)

response = client.responses.create(
    model=get_azure_openai_deployment_name(),
    tools=[
        {
            "type": "mcp",
            "server_label": "MicrosoftLearn",
            "server_url": "https://learn.microsoft.com/api/mcp",
            "allowed_tools": ["microsoft_docs_search", "microsoft_docs_search"],
            "require_approval": "never",
        },
    ],
    input="Provide a one-sentence summary of Azure AI Search, and provide a link to a Quickstart guide.",
)

print(response.output_text)

