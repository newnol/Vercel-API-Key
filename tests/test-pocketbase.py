"""
Test script for PocketBase using HTTP requests (like curl)
Tests connecting to PocketBase REST API and retrieving records from Vercel_api_key collection
"""

import requests
import json
import sys
from typing import Optional, Dict, Any

# PocketBase configuration
BASE_URL = 'https://base.selfhost.io.vn'
COLLECTION_NAME = 'Vercel_api_key'
API_BASE = f'{BASE_URL}/api/collections/{COLLECTION_NAME}'

# Authentication options
# Option 1: Direct token (if you have admin token)
TOKEN = None

# Option 2: Admin credentials for login
ADMIN_EMAIL = 'tantai13102005@gmail.com'
ADMIN_PASSWORD = 'ngotantai123'


def admin_login() -> Optional[str]:
    """Login as superuser admin and get auth token"""
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        return None
    
    try:
        # Use _superusers collection endpoint
        url = f'{BASE_URL}/api/collections/_superusers/auth-with-password'
        data = {
            'identity': ADMIN_EMAIL,
            'password': ADMIN_PASSWORD
        }
        
        print(f"\n🔐 Attempting superuser admin login...")
        print(f"   Email: {ADMIN_EMAIL}")
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('token')
            record = result.get('record', {})
            print(f"✅ Admin login successful!")
            print(f"   Token: {token[:30]}..." if token else "   No token found")
            print(f"   User ID: {record.get('id', 'N/A')}")
            return token
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None


def get_headers(use_bearer: bool = True) -> Dict[str, str]:
    """Get HTTP headers for requests
    Default to Bearer format as it works better with superuser tokens
    """
    headers = {
        'Content-Type': 'application/json',
    }
    # Add authentication token
    if TOKEN:
        if use_bearer:
            headers['Authorization'] = f'Bearer {TOKEN}'
        else:
            headers['Authorization'] = f'TOKEN {TOKEN}'
    return headers


def test_get_record(record_id: str, expand: Optional[str] = None, use_bearer: bool = True) -> Optional[Dict[str, Any]]:
    """
    Test getting a single record by ID
    Equivalent to: GET /api/collections/Vercel_api_key/records/{id}?expand=...
    """
    try:
        url = f'{API_BASE}/records/{record_id}'
        params = {}
        
        if expand:
            params['expand'] = expand
        
        print(f"\n📡 GET {url}")
        if params:
            print(f"   Query params: {params}")
        
        response = requests.get(url, headers=get_headers(use_bearer=use_bearer), params=params)
        
        if response.status_code == 200:
            record = response.json()
            print(f"\n✅ Record retrieved successfully:")
            print(json.dumps(record, indent=2, ensure_ascii=False))
            return record
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request error: {e}")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        return None


def test_list_records(page: int = 1, per_page: int = 10, expand: Optional[str] = None, use_bearer: bool = False) -> Optional[Dict[str, Any]]:
    """
    Test listing records from the collection
    Equivalent to: GET /api/collections/Vercel_api_key/records?page=1&perPage=10&expand=...
    """
    try:
        url = f'{API_BASE}/records'
        params = {
            'page': page,
            'perPage': per_page,
        }
        
        if expand:
            params['expand'] = expand
        
        print(f"\n📡 GET {url}")
        print(f"   Query params: {params}")
        print(f"   Auth format: {'Bearer' if use_bearer else 'TOKEN'}")
        
        response = requests.get(url, headers=get_headers(use_bearer=use_bearer), params=params)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get('items', [])
            total_items = data.get('totalItems', 0)
            
            print(f"\n✅ Found {len(records)} records (total: {total_items}):")
            for i, record in enumerate(records, 1):
                print(f"\n--- Record {i} ---")
                print(json.dumps(record, indent=2, ensure_ascii=False))
            
            return data
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request error: {e}")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        return None


def test_create_record(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Test creating a new record
    Equivalent to: POST /api/collections/Vercel_api_key/records
    """
    try:
        url = f'{API_BASE}/records'
        
        print(f"\n📡 POST {url}")
        print(f"   Body: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        response = requests.post(url, headers=get_headers(), json=data)
        
        if response.status_code == 200 or response.status_code == 201:
            record = response.json()
            print(f"\n✅ Record created successfully:")
            print(json.dumps(record, indent=2, ensure_ascii=False))
            return record
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request error: {e}")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
        return None


def show_curl_examples():
    """Show equivalent curl commands"""
    print("\n" + "="*60)
    print("Equivalent CURL commands:")
    print("="*60)
    
    print("\n1. List all records:")
    print(f"curl -X GET '{API_BASE}/records' \\")
    print("     -H 'Content-Type: application/json' \\")
    print(f"     -H 'Authorization: TOKEN {TOKEN}'")
    
    print("\n2. Get one record by ID:")
    print(f"curl -X GET '{API_BASE}/records/RECORD_ID?expand=relField1,relField2.subRelField' \\")
    print("     -H 'Content-Type: application/json' \\")
    print(f"     -H 'Authorization: TOKEN {TOKEN}'")
    
    print("\n3. Create a new record:")
    print(f"curl -X POST '{API_BASE}/records' \\")
    print("     -H 'Content-Type: application/json' \\")
    print(f"     -H 'Authorization: TOKEN {TOKEN}' \\")
    print("     -d '{\"name\": \"Test\", \"api_key\": \"vck_xxx\"}'")


if __name__ == "__main__":
    print("="*60)
    print("PocketBase Test Script (using HTTP requests)")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"API Endpoint: {API_BASE}")
    print("="*60)
    
    # Try admin login to get token
    admin_token = admin_login()
    if admin_token:
        # Update TOKEN globally for this session
        import sys
        module = sys.modules[__name__]
        module.TOKEN = admin_token
        print(f"\n✅ Using admin token: {admin_token[:30]}...")
    elif not TOKEN:
        print("\n⚠️  No authentication token available!")
        print("   Cannot proceed without authentication.")
        sys.exit(1)
    
    # Test 1: List all records (using Bearer format - works with superuser tokens)
    print("\n" + "="*60)
    print("TEST 1: List all records")
    print("="*60)
    result = test_list_records(page=1, per_page=10, use_bearer=True)
    
    # Test 2: Get first record if available
    if result and result.get('items'):
        first_record = result['items'][0]
        record_id = first_record.get('id')
        
        if record_id:
            print("\n" + "="*60)
            print(f"TEST 2: Get record by ID ({record_id})")
            print("="*60)
            test_get_record(record_id, use_bearer=True)
            
            print("\n" + "="*60)
            print(f"TEST 3: Get record with expand")
            print("="*60)
            test_get_record(record_id, expand='relField1,relField2.subRelField', use_bearer=True)
    else:
        print("\n⚠️  No records found. Cannot test get_one()")
        print("   You can manually test with:")
        print(f"   test_get_record('RECORD_ID', expand='relField1,relField2.subRelField')")
    
    # Show curl examples
    show_curl_examples()
    
    print("\n" + "="*60)
    print("Test completed!")
    print("="*60)
    print("\n💡 Tips:")
    print("   - To test with a specific record ID, call:")
    print("     test_get_record('YOUR_RECORD_ID', expand='relField1,relField2.subRelField')")
    print("   - To create a record, call:")
    print("     test_create_record({'name': 'Test', 'api_key': 'vck_xxx'})")
    print(f"   - Authentication token is configured: {TOKEN[:10]}...")
