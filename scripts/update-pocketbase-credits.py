import os
import sys
import requests
from dotenv import load_dotenv
import json

# Add parent directory to path to import pocketbase_client
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pocketbase_client import get_full_records_from_pocketbase, pocketbase_client

load_dotenv()

def fetch_credit_balance(api_key):
    """Fetch credit balance for a single API key."""
    try:
        response = requests.get(
            "https://ai-gateway.vercel.sh/v1/credits",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=10
        )
        if response.status_code == 200:
            credits = response.json()
            balance = float(credits.get("balance", 0))
            total_used = float(credits.get("total_used", 0))
            return balance, total_used
        else:
            print(f"❌ Failed to fetch credits for key: {response.status_code}")
            return 0.0, 0.0
    except Exception as e:
        print(f"❌ Error fetching credits: {e}")
        return 0.0, 0.0

def main():
    print("🔄 Fetching records from PocketBase...")
    records = get_full_records_from_pocketbase()

    if not records:
        print("❌ No records found in PocketBase")
        return

    print(f"📋 Found {len(records)} records")

    updated_count = 0
    for record in records:
        record_id = record.get("id")
        name = record.get("name", "Unknown")
        api_key = record.get("api_key", "")

        if not api_key:
            print(f"⚠️  Skipping {name}: no API key")
            continue

        print(f"🔍 Fetching credits for {name}...")
        balance, total_used = fetch_credit_balance(api_key)

        print(f"💰 {name}: Balance=${balance:.4f}, Used=${total_used:.4f}")

        # Update PocketBase record
        update_data = {
            "credit": balance,
            "total_used": total_used
        }

        success = pocketbase_client.update_key_sync(record_id, update_data)
        if success:
            updated_count += 1
        else:
            print(f"❌ Failed to update {name}")

    print(f"✅ Updated {updated_count}/{len(records)} records in PocketBase")

if __name__ == "__main__":
    main()
