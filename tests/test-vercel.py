import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


Vercel_api_key = os.getenv("Vercel_api_key")


client = OpenAI(
    api_key=Vercel_api_key,
    base_url='https://ai-gateway.vercel.sh/v1'
)

response = client.chat.completions.create(
    model='anthropic/claude-sonnet-4.5',
    messages=[
        {'role': 'user', 'content': 'Hello, world!'}
    ]
)

print(response.choices[0].message)
