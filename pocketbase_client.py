"""
PocketBase client for fetching Vercel API keys.
Handles authentication and caching of keys.
"""

import os
import httpx
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

# Configuration from environment variables
POCKETBASE_URL = os.getenv("POCKETBASE_URL", "https://base.selfhost.io.vn")
POCKETBASE_COLLECTION = os.getenv("POCKETBASE_COLLECTION", "Vercel_api_key")
POCKETBASE_EMAIL = os.getenv("POCKETBASE_EMAIL")
POCKETBASE_PASSWORD = os.getenv("POCKETBASE_PASSWORD")
POCKETBASE_TOKEN = os.getenv("POCKETBASE_TOKEN")  # Optional: direct token

# Cache settings
TOKEN_CACHE_TTL = 3600  # 1 hour
KEYS_CACHE_TTL = 300  # 5 minutes


class PocketBaseClient:
    """Client for interacting with PocketBase API."""
    
    def __init__(self):
        self.base_url = POCKETBASE_URL
        self.collection = POCKETBASE_COLLECTION
        self.api_base = f"{self.base_url}/api/collections/{self.collection}"
        self._token: Optional[str] = POCKETBASE_TOKEN
        self._token_expires_at: Optional[datetime] = None
        self._keys_cache: Optional[List[Dict[str, Any]]] = None
        self._keys_cache_expires_at: Optional[datetime] = None
        self._lock = asyncio.Lock()
    
    async def _get_auth_token(self) -> Optional[str]:
        """Get authentication token, using cache if available."""
        async with self._lock:
            # Use direct token if provided
            if self._token and not POCKETBASE_EMAIL:
                return self._token
            
            # Check if cached token is still valid
            if self._token and self._token_expires_at:
                if datetime.now() < self._token_expires_at:
                    return self._token
            
            # Login to get new token
            if not POCKETBASE_EMAIL or not POCKETBASE_PASSWORD:
                raise ValueError(
                    "PocketBase credentials not configured. "
                    "Set POCKETBASE_EMAIL and POCKETBASE_PASSWORD environment variables."
                )
            
            try:
                url = f"{self.base_url}/api/collections/_superusers/auth-with-password"
                data = {
                    "identity": POCKETBASE_EMAIL,
                    "password": POCKETBASE_PASSWORD
                }
                
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(url, json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        self._token = result.get("token")
                        # Cache token for 1 hour (PocketBase tokens typically last longer)
                        self._token_expires_at = datetime.now() + timedelta(seconds=TOKEN_CACHE_TTL)
                        print(f"✅ PocketBase authentication successful")
                        return self._token
                    else:
                        print(f"❌ PocketBase login failed: {response.status_code} - {response.text}")
                        return None
            except Exception as e:
                print(f"❌ PocketBase authentication error: {e}")
                return None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authentication."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}" if self._token else ""
        }
    
    async def fetch_keys(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Fetch Vercel API keys from PocketBase.
        Uses caching to avoid excessive API calls.
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            List of key dictionaries with structure:
            {
                "name": str,
                "api_key": str,
                "mail": str,
                ...
            }
        """
        async with self._lock:
            # Check cache
            if not force_refresh and self._keys_cache and self._keys_cache_expires_at:
                if datetime.now() < self._keys_cache_expires_at:
                    return self._keys_cache
            
            # Get auth token
            token = await self._get_auth_token()
            if not token:
                # Return cached keys if available, even if expired
                if self._keys_cache:
                    print("⚠️  Using stale cache due to auth failure")
                    return self._keys_cache
                raise Exception("Failed to authenticate with PocketBase")
            
            try:
                # Fetch all records (with pagination if needed)
                url = f"{self.api_base}/records"
                all_keys = []
                page = 1
                per_page = 100
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    while True:
                        params = {
                            "page": page,
                            "perPage": per_page
                        }
                        
                        response = await client.get(
                            url,
                            headers=self._get_headers(),
                            params=params
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            items = data.get("items", [])
                            all_keys.extend(items)
                            
                            total_items = data.get("totalItems", 0)
                            total_pages = data.get("totalPages", 1)
                            
                            if page >= total_pages or len(items) < per_page:
                                break
                            page += 1
                        elif response.status_code == 401:
                            # Token expired, try to refresh
                            print("⚠️  Token expired, refreshing...")
                            self._token = None
                            self._token_expires_at = None
                            token = await self._get_auth_token()
                            if not token:
                                raise Exception("Failed to refresh authentication token")
                            # Retry this page
                            continue
                        else:
                            error_msg = f"Failed to fetch keys: {response.status_code} - {response.text}"
                            print(f"❌ {error_msg}")
                            # Return cached keys if available
                            if self._keys_cache:
                                print("⚠️  Using stale cache due to fetch error")
                                return self._keys_cache
                            raise Exception(error_msg)
                
                # Transform to expected format
                formatted_keys = [
                    {
                        "name": k.get("name", "Unknown"),
                        "api_key": k.get("api_key", ""),
                        "mail": k.get("mail", ""),
                        "id": k.get("id", ""),
                        "created": k.get("created", ""),
                        "updated": k.get("updated", "")
                    }
                    for k in all_keys
                    if k.get("api_key")  # Only include keys with api_key
                ]
                
                # Update cache
                self._keys_cache = formatted_keys
                self._keys_cache_expires_at = datetime.now() + timedelta(seconds=KEYS_CACHE_TTL)
                
                print(f"✅ Fetched {len(formatted_keys)} Vercel keys from PocketBase")
                return formatted_keys
                
            except httpx.TimeoutException:
                error_msg = "PocketBase request timeout"
                print(f"❌ {error_msg}")
                if self._keys_cache:
                    print("⚠️  Using stale cache due to timeout")
                    return self._keys_cache
                raise Exception(error_msg)
            except Exception as e:
                error_msg = f"Error fetching keys from PocketBase: {e}"
                print(f"❌ {error_msg}")
                if self._keys_cache:
                    print("⚠️  Using stale cache due to error")
                    return self._keys_cache
                raise Exception(error_msg)
    
    async def test_connection(self) -> bool:
        """Test connection to PocketBase."""
        try:
            keys = await self.fetch_keys(force_refresh=True)
            return len(keys) > 0
        except Exception as e:
            print(f"❌ PocketBase connection test failed: {e}")
            return False

