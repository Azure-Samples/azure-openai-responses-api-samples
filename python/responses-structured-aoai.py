from openai import AzureOpenAI
from dotenv import load_dotenv
from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)

import os
import json

load_dotenv()

client = AzureOpenAI(
    api_key = get_azure_openai_api_key(),  
    api_version = get_azure_openai_api_version(),
    azure_endpoint = get_azure_openai_endpoint()
    )


response = client.responses.create(
    model=get_azure_openai_deployment_name(),
    input=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."}
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "calendar_event",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "date": {
                        "type": "string"
                    },
                    "participants": {
                        "type": "array", 
                        "items": {
                            "type": "string"
                        }
                    },
                },
                "required": ["name", "date", "participants"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

event = json.loads(response.output_text)

print(event)