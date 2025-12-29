from openai import OpenAI

client = OpenAI(
    api_key='sk-lb-LuVvR3CE-iKzPGHafeAP7xszMzDRaPCM',
    base_url='http://localhost:8000/v1',
)

completion = client.chat.completions.create(
    model='anthropic/claude-sonnet-4.5',
    reasoning_effort='medium',
    messages=[{'role': 'user', 'content': 'Hello! 1 + 1 = ?'}],
)

print(completion.choices[0].message.content)
