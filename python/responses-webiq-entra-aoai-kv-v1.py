import os
from openai import OpenAI
from azure.identity import (
    ClientSecretCredential,
    DefaultAzureCredential,
    get_bearer_token_provider,
)
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv

load_dotenv()

default_credential = DefaultAzureCredential()
azure_openai_token_provider = get_bearer_token_provider(
    default_credential, "https://cognitiveservices.azure.com/.default"
)

secret_client = SecretClient(
    vault_url=os.environ["KEY_VAULT_URL"],
    credential=default_credential,
)
webiq_client_secret = secret_client.get_secret(
    os.environ["WEBIQ_CLIENT_SECRET_NAME"]
).value

webiq_credential = ClientSecretCredential(
    tenant_id=os.environ["WEBIQ_TENANT_ID"],
    client_id=os.environ["WEBIQ_CLIENT_ID"],
    client_secret=webiq_client_secret,
)
webiq_access_token = webiq_credential.get_token(
    "https://api.microsoft.ai/.default"
).token

client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_V1_API_ENDPOINT"],
    api_key=azure_openai_token_provider,
)

response = client.responses.create(
    model=os.environ["AZURE_OPENAI_API_MODEL"],
    tools=[
        {
            "type": "mcp",
            "server_label": "WebIQ",
            "server_url": "https://api.microsoft.ai/v3/mcp",
            "require_approval": "never",
            "authorization": webiq_access_token,
        },
    ],
    input="What is the latest image-gen model from MAI?",
)

print(response.output_text)
