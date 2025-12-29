"""
Test OpenAI API Compatibility
Kiểm tra format response có đúng chuẩn OpenAI không
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"
VALID_API_KEY = os.getenv("API_KEY_TEST")

def print_json(data, title="Response"):
    """Pretty print JSON"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print('='*60)
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_chat_completion():
    """Test chat completion response format"""
    print("\n🧪 Test 1: Chat Completion (Valid Request)")
    
    response = requests.post(
        f"{BASE_URL}/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {VALID_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": "Say 'test' only"}],
            "max_tokens": 10
        }
    )
    
    data = response.json()
    print_json(data, "Chat Completion Response")
    
    # Kiểm tra format
    required_fields = ["id", "object", "created", "model", "choices"]
    missing = [f for f in required_fields if f not in data]
    
    if missing:
        print(f"❌ Missing required fields: {missing}")
    else:
        print("✅ Response format correct! Has all required fields.")
    
    # Kiểm tra usage
    if "usage" in data:
        usage_fields = ["prompt_tokens", "completion_tokens", "total_tokens"]
        usage_missing = [f for f in usage_fields if f not in data["usage"]]
        if usage_missing:
            print(f"⚠️  Usage missing fields: {usage_missing}")
        else:
            print("✅ Usage format correct!")
    
    return response.status_code == 200

def test_invalid_api_key():
    """Test error response with invalid API key"""
    print("\n🧪 Test 2: Invalid API Key (Error Format)")
    
    response = requests.post(
        f"{BASE_URL}/v1/chat/completions",
        headers={
            "Authorization": "Bearer invalid-key-12345",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )
    
    data = response.json()
    print_json(data, f"Error Response (Status: {response.status_code})")
    
    # Kiểm tra OpenAI error format
    if "error" in data:
        error = data["error"]
        required_error_fields = ["message", "type", "param", "code"]
        missing = [f for f in required_error_fields if f not in error]
        
        if missing:
            print(f"❌ Error missing fields: {missing}")
        else:
            print("✅ Error format correct! Has all required fields (message, type, param, code)")
    else:
        print("❌ Response does not have 'error' field")
    
    return response.status_code == 401

def test_missing_auth():
    """Test error response with missing Authorization header"""
    print("\n🧪 Test 3: Missing Authorization (Error Format)")
    
    response = requests.post(
        f"{BASE_URL}/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )
    
    data = response.json()
    print_json(data, f"Error Response (Status: {response.status_code})")
    
    # Kiểm tra format
    if "error" in data and all(k in data["error"] for k in ["message", "type", "param", "code"]):
        print("✅ Error format correct!")
    else:
        print("❌ Error format incorrect")
    
    return response.status_code == 401

def test_models_endpoint():
    """Test /v1/models endpoint"""
    print("\n🧪 Test 4: List Models Endpoint")
    
    response = requests.get(
        f"{BASE_URL}/v1/models",
        headers={"Authorization": f"Bearer {VALID_API_KEY}"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        # Only show first 3 models if there are many
        if "data" in data and len(data["data"]) > 3:
            preview = {"object": data.get("object"), "data": data["data"][:3], "...": f"and {len(data['data'])-3} more models"}
            print_json(preview, "Models Response (truncated)")
        else:
            print_json(data, "Models Response")
        print("✅ Models endpoint works!")
    else:
        print_json(response.json(), "Error")
    
    return response.status_code == 200

def main():
    print("=" * 60)
    print("🔍 OpenAI API Compatibility Test")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"API Key: {VALID_API_KEY[:20]}..." if VALID_API_KEY else "API Key: Not set!")
    
    if not VALID_API_KEY:
        print("\n❌ Please set API_KEY_TEST in .env file")
        return
    
    results = []
    
    # Run tests
    results.append(("Chat Completion", test_chat_completion()))
    results.append(("Invalid API Key", test_invalid_api_key()))
    results.append(("Missing Auth", test_missing_auth()))
    results.append(("List Models", test_models_endpoint()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
    
    passed_count = sum(1 for _, p in results if p)
    print(f"\n  Total: {passed_count}/{len(results)} tests passed")

if __name__ == "__main__":
    main()

