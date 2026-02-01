import base64
from openai import OpenAI
import os
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

with open("../assets/employee_handbook.pdf", "rb") as f: # assumes PDF is in the assets directory
    data = f.read()

base64_string = base64.b64encode(data).decode("utf-8")

response = client.responses.create(
    model=get_azure_openai_deployment_name(),
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "filename": "employee_handbook.pdf",
                    "file_data": f"data:application/pdf;base64,{base64_string}",
                },
                {
                    "type": "input_text",
                    "text": "What are the company values?",
                },
            ],
        },
    ]
)

print(response.output_text)