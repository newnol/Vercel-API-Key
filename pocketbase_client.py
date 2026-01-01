"""
PocketBase client for fetching Vercel API keys.
Handles authentication and caching of keys.
"""

import os
import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

# Configuration from environment variables
POCKETBASE_URL = os.getenv("POCKETBASE_URL", "https://base.selfhost.io.vn")
POCKETBASE_COLLECTION = os.getenv("POCKETBASE_COLLECTION", "Vercel_api_key")
POCKETBASE_EMAIL = os.getenv("POCKETBASE_EMAIL")
POCKETBASE_PASSWORD = os.getenv("POCKETBASE_PASSWORD")

# Cache settings
TOKEN_CACHE_TTL = 3600  # 1 hour
KEYS_CACHE_TTL = 300  # 5 minutes


class PocketBaseClient:
    """Client for interacting with PocketBase API (sync version)."""

    def __init__(self):
        self.base_url = POCKETBASE_URL
        self.collection = POCKETBASE_COLLECTION
        self.api_base = f"{self.base_url}/api/collections/{self.collection}"
        self._token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        self._keys_cache: Optional[List[Dict[str, Any]]] = None
        self._keys_cache_expires_at: Optional[datetime] = None

    def _login(self) -> Optional[str]:
        """Login to PocketBase and get auth token."""
        if not POCKETBASE_EMAIL or not POCKETBASE_PASSWORD:
            print("❌ PocketBase credentials not configured")
            return None

        try:
            url = f"{self.base_url}/api/collections/_superusers/auth-with-password"
            data = {
                "identity": POCKETBASE_EMAIL,
                "password": POCKETBASE_PASSWORD
            }

            with httpx.Client(timeout=10.0) as client:
                response = client.post(url, json=data)

                if response.status_code == 200:
                    result = response.json()
                    self._token = result.get("token")
                    self._token_expires_at = datetime.now() + timedelta(seconds=TOKEN_CACHE_TTL)
                    print(f"✅ PocketBase authentication successful")
                    return self._token
                else:
                    print(f"❌ PocketBase login failed: {response.status_code}")
                    return None
        except Exception as e:
            print(f"❌ PocketBase authentication error: {e}")
            return None

    def _get_token(self) -> Optional[str]:
        """Get valid auth token, refreshing if needed."""
        # Check if token is still valid
        if self._token and self._token_expires_at:
            if datetime.now() < self._token_expires_at:
                return self._token

        # Need to login
        return self._login()

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authentication."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}" if self._token else ""
        }

    def fetch_keys_sync(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Fetch Vercel API keys from PocketBase (synchronous).
        Uses caching to avoid excessive API calls.
        """
        # Check cache
        if not force_refresh and self._keys_cache and self._keys_cache_expires_at:
            if datetime.now() < self._keys_cache_expires_at:
                return self._keys_cache

        # Get auth token
        token = self._get_token()
        if not token:
            if self._keys_cache:
                print("⚠️  Using stale cache due to auth failure")
                return self._keys_cache
            return []

        try:
            url = f"{self.api_base}/records"
            all_keys = []
            page = 1
            per_page = 100

            with httpx.Client(timeout=30.0) as client:
                while True:
                    params = {"page": page, "perPage": per_page}
                    response = client.get(url, headers=self._get_headers(), params=params)

                    if response.status_code == 200:
                        data = response.json()
                        items = data.get("items", [])
                        all_keys.extend(items)

                        total_pages = data.get("totalPages", 1)
                        if page >= total_pages or len(items) < per_page:
                            break
                        page += 1
                    elif response.status_code == 401:
                        # Token expired, refresh
                        print("⚠️  Token expired, refreshing...")
                        self._token = None
                        token = self._get_token()
                        if not token:
                            break
                        continue
                    else:
                        print(f"❌ Failed to fetch keys: {response.status_code}")
                        break

            # Transform to expected format
            formatted_keys = [
                {
                    "name": k.get("name", "Unknown"),
                    "api_key": k.get("api_key", ""),
                    "mail": k.get("mail", ""),
                }
                for k in all_keys
                if k.get("api_key")
            ]

            # Update cache
            if formatted_keys:
                self._keys_cache = formatted_keys
                self._keys_cache_expires_at = datetime.now() + timedelta(seconds=KEYS_CACHE_TTL)
                print(f"✅ Fetched {len(formatted_keys)} Vercel keys from PocketBase")

            return formatted_keys

        except Exception as e:
            print(f"❌ Error fetching keys from PocketBase: {e}")
            if self._keys_cache:
                print("⚠️  Using stale cache due to error")
                return self._keys_cache
            return []

    def test_connection(self) -> bool:
        """Test connection to PocketBase."""
        try:
            keys = self.fetch_keys_sync(force_refresh=True)
            return len(keys) > 0
        except Exception as e:
            print(f"❌ PocketBase connection test failed: {e}")
            return False


# Global instance
pocketbase_client = PocketBaseClient()


def get_keys_from_pocketbase() -> List[Dict[str, Any]]:
    """Helper function to get keys from PocketBase."""
    return pocketbase_client.fetch_keys_sync()
