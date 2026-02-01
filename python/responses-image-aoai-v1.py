from openai import OpenAI
from dotenv import load_dotenv
from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)

import os
import base64

load_dotenv()

IMAGE_PATH = "../assets/book.jpeg"

client = OpenAI(
    api_key=get_azure_openai_api_key(),
    base_url=get_azure_openai_v1_base_url(),

)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image(IMAGE_PATH)

response = client.responses.create(
    model=get_azure_openai_deployment_name(),
    input=[
        {"role": "user", "content": "Identify the bird on the front of this book cover."},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{base64_image}"
                }
            ]
        }
    ]
)

print(response.output_text)