from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    api_key = os.environ["AZURE_OPENAI_API_KEY"],  
    api_version = os.environ["AZURE_OPENAI_API_VERSION"],
    azure_endpoint = os.environ["AZURE_OPENAI_API_ENDPOINT"]
    )

response = client.responses.create(
    model=os.environ["AZURE_OPENAI_API_MODEL"],
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "Describe this image" },
                {
                    "type": "input_image",
                    "image_url": "https://learn.microsoft.com/azure/well-architected/ai/images/responsible-ai.png"
                }
            ]
        }
    ]
)

print(response.output_text)

