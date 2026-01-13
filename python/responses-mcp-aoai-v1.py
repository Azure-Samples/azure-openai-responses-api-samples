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

