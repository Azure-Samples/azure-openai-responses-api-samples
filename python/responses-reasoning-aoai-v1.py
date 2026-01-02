import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_V1_API_ENDPOINT"),
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