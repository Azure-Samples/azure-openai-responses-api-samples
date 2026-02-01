import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from sample_env import (
    get_azure_openai_api_key,
    get_azure_openai_api_version,
    get_azure_openai_endpoint,
    get_azure_openai_deployment_name,
    get_azure_openai_v1_base_url,
)


load_dotenv()

client = AzureOpenAI(
    api_key = get_azure_openai_api_key(),  
    api_version = get_azure_openai_api_version(),
    azure_endpoint = get_azure_openai_endpoint()
    )

response = client.responses.create(
    model="gpt-5-mini",
    input="How much wood would a woodchuck chuck?",
    reasoning={
        "effort": "low",
        "summary": "auto", # auto, concise, or detailed, gpt-5 series do not support concise
    }
)

# Extract and print reasoning summary (Optional)
reasoning_summaries = []

for item in response.output:
    if getattr(item, "type", None) == "reasoning":
        for part in (item.summary or []):
            if getattr(part, "type", None) == "summary_text":
                reasoning_summaries.append(part.text)

print("=== Reasoning summary ===")
print("\n\n".join(reasoning_summaries) if reasoning_summaries else "(none)")

# Print results
print("\n=== Final answer ===")
print(response.output_text)