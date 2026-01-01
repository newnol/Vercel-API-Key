"""
Test script to verify PocketBase connection and key fetching.
Run this before starting the server to ensure PocketBase is configured correctly.
"""

import asyncio
import os
from dotenv import load_dotenv
from pocketbase_client import PocketBaseClient

load_dotenv()


async def test_pocketbase():
    """Test PocketBase connection and key fetching."""
    print("=" * 60)
    print("PocketBase Connection Test")
    print("=" * 60)

    # Check environment variables
    print("\n📋 Checking environment variables...")
    required_vars = [
        "POCKETBASE_URL",
        "POCKETBASE_COLLECTION",
        "POCKETBASE_EMAIL",
        "POCKETBASE_PASSWORD"
    ]

    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"  ❌ {var}: Not set")
        else:
            # Mask sensitive values
            if "PASSWORD" in var:
                print(f"  ✅ {var}: {'*' * len(value)}")
            else:
                print(f"  ✅ {var}: {value}")

    if missing_vars:
        print(f"\n❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("   Please set them in your .env file")
        return False

    # Test connection
    print("\n🔌 Testing PocketBase connection...")
    client = PocketBaseClient()

    try:
        # Test fetching keys
        print("  Fetching keys from PocketBase...")
        keys = await client.fetch_keys(force_refresh=True)

        if not keys:
            print("  ⚠️  No keys found in PocketBase collection")
            print("     Please add at least one Vercel API key to the collection")
            return False

        print(f"  ✅ Successfully fetched {len(keys)} keys:")
        for i, key in enumerate(keys, 1):
            print(f"     {i}. {key['name']} ({key.get('mail', 'N/A')})")
            print(f"        API Key: {key['api_key'][:20]}...")

        print("\n✅ PocketBase connection test passed!")
        print("   Server is ready to use PocketBase for key management")
        return True

    except Exception as e:
        print(f"\n❌ Error connecting to PocketBase: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check if PocketBase URL is correct")
        print("   2. Verify email and password are correct")
        print("   3. Ensure collection name matches your PocketBase collection")
        print("   4. Check network connectivity to PocketBase server")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_pocketbase())
    exit(0 if success else 1)
