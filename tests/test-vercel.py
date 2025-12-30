import os
from openai import OpenAI
 
client = OpenAI(
    api_key="vck_0GyhZ4bhPplVvBebkyJUwUOLDPRcnGIXRy7OsuFkmuS68iaMQz3NjwV2",
    base_url='https://ai-gateway.vercel.sh/v1'
)
 
response = client.chat.completions.create(
    model='anthropic/claude-sonnet-4.5',
    messages=[
        {'role': 'user', 'content': 'Hello, world!'}
    ]
)

print(response.choices[0].message)