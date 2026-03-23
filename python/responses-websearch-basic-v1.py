import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
 api_key=os.getenv("AZURE_OPENAI_API_KEY"),
 base_url=os.getenv("AZURE_OPENAI_V1_API_ENDPOINT"),
)
response = client.responses.create( 
 model=os.getenv("AZURE_OPENAI_API_MODEL"),
 tools=[{"type": "web_search"}],
 input="Who won the most recent Formula 1 race?"
)
print(response.output_text)
#print(response)