from openai import OpenAI
import dotenv
import os
import time
dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY_TEST')

client = OpenAI(
    api_key=API_KEY,
    base_url='http://localhost:8000/v1',
)

completion = client.chat.completions.create(
  model="anthropic/claude-sonnet-4.5",
  messages=[
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)