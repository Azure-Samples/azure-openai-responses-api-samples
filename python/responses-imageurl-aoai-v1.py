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
