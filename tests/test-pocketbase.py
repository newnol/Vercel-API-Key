"""
Test script for PocketBase integration.
Run this to verify PocketBase connection before starting the server.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from pocketbase_client import pocketbase_client, POCKETBASE_URL, POCKETBASE_EMAIL


def test_pocketbase():
    """Test PocketBase connection and key fetching."""
    print("=" * 60)
    print("PocketBase Connection Test")
    print("=" * 60)
    
    # Check environment variables
    print("\n📋 Checking configuration...")
    print(f"   URL: {POCKETBASE_URL}")
    print(f"   Email: {POCKETBASE_EMAIL or 'Not set'}")
    print(f"   Password: {'*****' if os.getenv('POCKETBASE_PASSWORD') else 'Not set'}")
    
    if not POCKETBASE_EMAIL or not os.getenv("POCKETBASE_PASSWORD"):
        print("\n❌ Missing PocketBase credentials!")
        print("   Set POCKETBASE_EMAIL and POCKETBASE_PASSWORD in .env")
        return False
    
    # Test connection
    print("\n🔌 Testing connection...")
    success = pocketbase_client.test_connection()
    
    if success:
        print("\n✅ PocketBase connection test PASSED!")
        
        # Show keys
        keys = pocketbase_client.fetch_keys_sync()
        print(f"\n📋 Found {len(keys)} keys:")
        for i, key in enumerate(keys, 1):
            print(f"   {i}. {key['name']} ({key.get('mail', 'N/A')})")
        
        return True
    else:
        print("\n❌ PocketBase connection test FAILED!")
        return False


if __name__ == "__main__":
    success = test_pocketbase()
    sys.exit(0 if success else 1)
