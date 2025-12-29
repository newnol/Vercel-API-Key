from openai import OpenAI

client = OpenAI(
    api_key='sk-lb-JvyUvt9xdADNUOrq_U_PaGqpGh8RrZkL',
    base_url='http://localhost:8000/v1',
)

completion = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': 'Hello! 1 + 1 = ?'}],
)

print(completion.choices[0].message.content)
