import os
import litellm
from dotenv import load_dotenv
import json

load_dotenv()

# Configure LiteLLM to use our local proxy
# Note: LiteLLM usually expects "openai/<model>" or just "<model>"
# We will point it to our local server
litellm.api_base = "http://localhost:8001/v1"
litellm.api_key = os.getenv("API_KEY_TEST", "test-key")
litellm.drop_params = True # Drop unsupported params if any

def print_json(data, title="Response"):
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print('='*60)
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))

def test_litellm_thinking():
    print("\n🧠 Testing LiteLLM Compatibility with Thinking Model...")

    # We use the 'openai/' prefix so LiteLLM treats it as an OpenAI-compatible endpoint
    # but we pass our custom model name
    model = "openai/anthropic/claude-sonnet-4.5-thinking"

    print(f"Sending request via LiteLLM with model: {model}")

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "What is the capital of France? Think about it."
                }
            ],
            stream=False
        )

        print("\n✅ LiteLLM Request Successful!")

        # Convert ModelResponse to dict for printing
        response_dict = response.model_dump() if hasattr(response, 'model_dump') else dict(response)
        print_json(response_dict, "LiteLLM Response")

        # Check if reasoning is present in the message content or extra fields
        # Note: The server injects reasoning into the request to Vercel.
        # The response from Vercel (Claude) usually contains the reasoning in the content
        # or as a separate field depending on how Vercel/Claude returns it.
        # In the previous user output, we saw "reasoning" field in the message object.

        choices = response_dict.get('choices', [])
        if choices:
            message = choices[0].get('message', {})
            content = message.get('content', '')
            reasoning = message.get('reasoning')

            print(f"\nContent length: {len(content)}")
            if reasoning:
                print(f"✅ Reasoning field found: {reasoning[:100]}...")
            else:
                print("⚠️ No 'reasoning' field found in message object (this might be normal if provider returns it in content)")

    except Exception as e:
        print(f"\n❌ LiteLLM Error: {e}")

if __name__ == "__main__":
    test_litellm_thinking()
