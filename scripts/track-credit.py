import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

total = 0
balance = 0

with open("key-list.json", "r") as f:
    key_list = json.load(f)

for key in key_list["keys"]:
    print(key["name"])
    print(key["mail"])
    print("--------------------------------")
    response = requests.get(
        "https://ai-gateway.vercel.sh/v1/credits",
        headers={
            "Authorization": f"Bearer {key['api_key']}",
            "Content-Type": "application/json",
        },
    )
    credits = response.json()
    # Convert to float in case credits["total_used"] is string
    try:
        balance += float(credits["balance"])
        used_credits = float(credits["total_used"])
    except (ValueError, TypeError):
        used_credits = 0.0
    total += used_credits
    print(credits)
    print(balance)

print(total)