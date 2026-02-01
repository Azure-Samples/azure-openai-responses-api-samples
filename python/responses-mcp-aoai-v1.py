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
    tools=[
        {
            "type": "mcp",
            "server_label": "MicrosoftLearn",
            "server_url": "https://learn.microsoft.com/api/mcp",
            "allowed_tools": ["microsoft_docs_search", "microsoft_docs_search"],
            "require_approval": "never",
        },
    ],
    input="Provide a one-sentence summary of the Microsoft Agent Framework, and provide a link to a Quickstart guide.",
)

print(response.output_text)

