import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8001"
# Sử dụng key test từ env hoặc key mặc định
API_KEY = os.getenv("API_KEY_TEST", "test-key")

def print_json(data, title="Response"):
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print('='*60)
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_thinking_model():
    print("\n🧠 Testing Thinking Model Request...")

    # Model có đuôi -thinking
    model = "anthropic/claude-sonnet-4.5-thinking"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": "What is 2+2? Think about it."
            }
        ],
        "stream": False
    }

    print(f"Sending request with model: {model}")
    print("Expected behavior: Server removes '-thinking' and adds reasoning parameters.")

    try:
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            print_json(data, "Success Response")
            print("\n✅ Request sent successfully!")
        else:
            print(f"\n❌ Request failed with status {response.status_code}")
            try:
                print_json(response.json(), "Error Details")
            except:
                print(response.text)

    except Exception as e:
        print(f"\n❌ Error sending request: {e}")
        print("Make sure the server is running on localhost:8000")

if __name__ == "__main__":
    test_thinking_model()
