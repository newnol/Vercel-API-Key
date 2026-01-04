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
                    "content": "What is 2+2? Think about it."
                }
            ],
            stream=True
        )

        print("\n✅ LiteLLM Request Successful!")
        print("\n--- Stream Output ---")

        for chunk in response:
            delta = chunk.choices[0].delta
            content = delta.content
            reasoning = getattr(delta, "reasoning_content", None) or getattr(delta, "reasoning", None)

            if content:
                print(content, end="", flush=True)
            if reasoning:
                # Print reasoning in a different way to distinguish?
                # For now just print it to stderr or log it
                pass

        print("\n[DONE]")

    except Exception as e:
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
