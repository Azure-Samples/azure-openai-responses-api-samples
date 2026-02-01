import os
import json
import requests
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

def get_weather(latitude: float, longitude: float) -> str:
    """Return a short natural language weather summary for given coordinates."""
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m",
        },
        timeout=10,
    )
    c = r.json().get("current", {})
    temp = c.get("temperature_2m")
    wind = c.get("wind_speed_10m")
    return f"Current temperature is {temp}°C with wind {wind} m/s." if temp is not None else "Weather data unavailable."

client = OpenAI(
    api_key=get_azure_openai_api_key(),
    base_url=get_azure_openai_v1_base_url(),
)

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current temperature (C) & wind for coordinates.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
            },
            "required": ["latitude", "longitude"],
        },
    }
]

# Running conversation state
conversation = [
    {"role": "user", "content": "What's the weather in London right now?"}
]

# First model call – model decides whether to call the tool
resp1 = client.responses.create(
    model=get_azure_openai_deployment_name(),
    tools=tools,
    input=conversation,
)

# Add model output messages (may include a function_call) to the conversation
conversation += resp1.output

# Execute any function calls and append outputs
for item in resp1.output:
    if item.type == "function_call" and item.name == "get_weather":
        args = json.loads(item.arguments)
        weather_text = get_weather(args["latitude"], args["longitude"])
        conversation.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps({"weather": weather_text}),
        })

# Second model call – model incorporates tool output and answers user
final_resp = client.responses.create(
    model=get_azure_openai_deployment_name(),
    tools=tools,
    instructions="Answer using the weather tool output only; be concise.",
    input=conversation,
)

print(final_resp.output_text)
