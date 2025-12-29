"""
Vercel AI Gateway Load Balancer Server
A FastAPI server that acts as a reverse proxy with credit-based load balancing.
"""

import json
import asyncio
import time
import random
import os
from contextlib import asynccontextmanager
from typing import Optional
from datetime import datetime, timedelta, timezone

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, Response, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from database import (
    init_database, create_key, list_keys, get_key_by_id,
    update_key, delete_key, get_key_stats, log_usage
)
from auth import AuthMiddleware

load_dotenv()

# === Configuration ===
KEY_LIST_PATH = "config/key-list.json"
VERCEL_GATEWAY_URL = "https://ai-gateway.vercel.sh"
CREDIT_CACHE_TTL = 300  # 5 minutes
MIN_CREDIT = 0.01

# === Pydantic Models for Admin API ===
class CreateKeyRequest(BaseModel):
    name: str
    rate_limit: int = 0  # 0 = unlimited
    expires_in_days: Optional[int] = None

class UpdateKeyRequest(BaseModel):
    name: Optional[str] = None
    rate_limit: Optional[int] = None
    is_active: Optional[bool] = None
    expires_in_days: Optional[int] = None

# === Vercel Key Manager ===
class VercelKeyManager:
    """Manages Vercel API keys and their credit balances."""
    
    def __init__(self):
        self.keys: list[dict] = []
        self._lock = asyncio.Lock()
        self._load_keys()
    
    def _load_keys(self):
        """Load Vercel keys from JSON file."""
        try:
            with open(KEY_LIST_PATH) as f:
                data = json.load(f)
            self.keys = [
                {
                    "name": k["name"],
                    "api_key": k["api_key"],
                    "balance": 0.0,
                    "total_used": 0.0,
                    "updated_at": 0
                }
                for k in data["keys"]
            ]
        except FileNotFoundError:
            print(f"Warning: {KEY_LIST_PATH} not found. No Vercel keys loaded.")
            self.keys = []
    
    async def _fetch_credit(self, key: dict) -> None:
        """Fetch credit balance for a single key."""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{VERCEL_GATEWAY_URL}/v1/credits",
                    headers={"Authorization": f"Bearer {key['api_key']}"},
                    timeout=10
                )
                if resp.status_code == 200:
                    data = resp.json()
                    key["balance"] = float(data.get("balance", 0))
                    key["total_used"] = float(data.get("total_used", 0))
                    key["updated_at"] = time.time()
        except Exception as e:
            print(f"Error fetching credit for {key['name']}: {e}")
    
    async def refresh_all(self):
        """Refresh credit balance for all keys."""
        await asyncio.gather(*[self._fetch_credit(k) for k in self.keys])
        print(f"Refreshed credits for {len(self.keys)} Vercel keys")
    
    async def get_key(self) -> Optional[str]:
        """
        Select a Vercel key using weighted random based on balance.
        Keys with higher balance have higher probability of being selected.
        """
        async with self._lock:
            now = time.time()
            
            # Refresh stale keys
            for key in self.keys:
                if now - key["updated_at"] > CREDIT_CACHE_TTL:
                    await self._fetch_credit(key)
            
            # Filter keys with sufficient balance
            available = [k for k in self.keys if k["balance"] > MIN_CREDIT]
            
            if not available:
                return None
            
            # Weighted random selection
            total = sum(k["balance"] for k in available)
            if total == 0:
                return random.choice(available)["api_key"]
            
            r = random.uniform(0, total)
            cumulative = 0
            for key in available:
                cumulative += key["balance"]
                if r <= cumulative:
                    print(f"Selected Vercel key: {key['name']} (${key['balance']:.4f})")
                    return key["api_key"]
            
            return available[-1]["api_key"]
    
    def get_status(self) -> list[dict]:
        """Get status of all Vercel keys."""
        return [
            {
                "name": k["name"],
                "balance": k["balance"],
                "total_used": k["total_used"],
                "last_updated": datetime.fromtimestamp(k["updated_at"]).isoformat() if k["updated_at"] else None
            }
            for k in self.keys
        ]

# === Global instances ===
vercel_key_manager = VercelKeyManager()

# === Lifespan ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize on startup, cleanup on shutdown."""
    # Initialize database
    await init_database()
    print("Database initialized")
    
    # Refresh Vercel key credits
    await vercel_key_manager.refresh_all()
    
    # Start background refresh task
    async def periodic_refresh():
        while True:
            await asyncio.sleep(CREDIT_CACHE_TTL)
            await vercel_key_manager.refresh_all()
    
    task = asyncio.create_task(periodic_refresh())
    
    yield
    
    # Cleanup
    task.cancel()

# === FastAPI App ===
app = FastAPI(
    title="Vercel AI Gateway Load Balancer",
    description="Load balanced proxy for Vercel AI Gateway with API key authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Add authentication middleware
app.add_middleware(AuthMiddleware)

# === Health & Utility Endpoints ===
@app.get("/health")
async def health():
    """Basic health check."""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()}

@app.get("/lb/health")
async def lb_health():
    """Detailed health check with Vercel key status."""
    return {
        "status": "ok",
        "vercel_keys": vercel_key_manager.get_status(),
        "total_balance": sum(k["balance"] for k in vercel_key_manager.keys),
        "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    }

@app.post("/lb/refresh")
async def lb_refresh():
    """Force refresh Vercel key credits."""
    await vercel_key_manager.refresh_all()
    return {"message": "Credits refreshed", "keys_count": len(vercel_key_manager.keys)}

# === Admin API Endpoints ===
@app.post("/admin/keys")
async def admin_create_key(req: CreateKeyRequest):
    """Create a new client API key."""
    raw_key, api_key = await create_key(
        name=req.name,
        rate_limit=req.rate_limit,
        expires_in_days=req.expires_in_days
    )
    
    return {
        "message": "API key created successfully",
        "key": raw_key,  # Only shown once!
        "key_info": {
            "id": api_key.id,
            "name": api_key.name,
            "rate_limit": api_key.rate_limit,
            "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
            "created_at": api_key.created_at.isoformat()
        },
        "warning": "Save this key now. It will not be shown again!"
    }

@app.get("/admin/keys")
async def admin_list_keys():
    """List all client API keys."""
    keys = await list_keys()
    return {
        "keys": [
            {
                "id": k.id,
                "name": k.name,
                "rate_limit": k.rate_limit,
                "is_active": k.is_active,
                "expires_at": k.expires_at.isoformat() if k.expires_at else None,
                "created_at": k.created_at.isoformat()
            }
            for k in keys
        ],
        "total": len(keys)
    }

@app.get("/admin/keys/{key_id}")
async def admin_get_key(key_id: str):
    """Get details and usage stats for a specific key."""
    api_key = await get_key_by_id(key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="Key not found")
    
    stats = await get_key_stats(key_id)
    
    return {
        "key_info": {
            "id": api_key.id,
            "name": api_key.name,
            "rate_limit": api_key.rate_limit,
            "is_active": api_key.is_active,
            "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
            "created_at": api_key.created_at.isoformat()
        },
        "stats": stats
    }

@app.patch("/admin/keys/{key_id}")
async def admin_update_key(key_id: str, req: UpdateKeyRequest):
    """Update a client API key."""
    # Check if key exists
    existing = await get_key_by_id(key_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Key not found")
    
    # Calculate expires_at if expires_in_days provided
    expires_at = None
    if req.expires_in_days is not None:
        if req.expires_in_days > 0:
            expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=req.expires_in_days)
    
    updated = await update_key(
        key_id=key_id,
        name=req.name,
        rate_limit=req.rate_limit,
        is_active=req.is_active,
        expires_at=expires_at
    )
    
    return {
        "message": "Key updated successfully",
        "key_info": {
            "id": updated.id,
            "name": updated.name,
            "rate_limit": updated.rate_limit,
            "is_active": updated.is_active,
            "expires_at": updated.expires_at.isoformat() if updated.expires_at else None
        }
    }

@app.delete("/admin/keys/{key_id}")
async def admin_delete_key(key_id: str):
    """Delete a client API key."""
    success = await delete_key(key_id)
    if not success:
        raise HTTPException(status_code=404, detail="Key not found")
    
    return {"message": "Key deleted successfully", "key_id": key_id}

# === Passthrough Proxy ===
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy(path: str, request: Request):
    """
    Proxy all requests to Vercel AI Gateway.
    Automatically selects the best Vercel key based on credit balance.
    """
    # Get Vercel API key
    vercel_api_key = await vercel_key_manager.get_key()
    
    if not vercel_api_key:
        return JSONResponse(
            status_code=503,
            content={
                "error": {
                    "message": "No available Vercel API keys with sufficient credit",
                    "type": "server_error"
                }
            }
        )
    
    # Clone headers, replace Authorization with Vercel key
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "authorization", "content-length")
    }
    headers["Authorization"] = f"Bearer {vercel_api_key}"
    
    # Build URL with query params
    url = f"{VERCEL_GATEWAY_URL}/{path}"
    if request.query_params:
        url += f"?{request.query_params}"
    
    # Get request body
    body = await request.body()
    
    # Check if streaming is requested
    is_stream = False
    model = None
    if body:
        try:
            data = json.loads(body)
            is_stream = data.get("stream", False)
            model = data.get("model")
        except:
            pass
    
    # Log usage with model info
    if hasattr(request.state, "api_key") and request.state.api_key:
        await log_usage(
            key_id=request.state.api_key.id,
            endpoint=f"/{path}",
            model=model
        )
    
    async with httpx.AsyncClient() as client:
        try:
            if is_stream:
                # Streaming response
                async def stream_generator():
                    async with client.stream(
                        method=request.method,
                        url=url,
                        headers=headers,
                        content=body,
                        timeout=300  # 5 minutes for long generations
                    ) as resp:
                        async for chunk in resp.aiter_bytes():
                            yield chunk
                
                return StreamingResponse(
                    stream_generator(),
                    media_type="text/event-stream",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "X-Accel-Buffering": "no"
                    }
                )
            else:
                # Regular response
                resp = await client.request(
                    method=request.method,
                    url=url,
                    headers=headers,
                    content=body,
                    timeout=300
                )
                
                # Try to extract token usage for logging
                if hasattr(request.state, "api_key") and request.state.api_key:
                    try:
                        resp_data = resp.json()
                        if "usage" in resp_data:
                            tokens = resp_data["usage"].get("total_tokens")
                            if tokens:
                                await log_usage(
                                    key_id=request.state.api_key.id,
                                    endpoint=f"/{path}",
                                    tokens_used=tokens,
                                    model=model
                                )
                    except:
                        pass
                
                return Response(
                    content=resp.content,
                    status_code=resp.status_code,
                    media_type=resp.headers.get("content-type", "application/json")
                )
        
        except httpx.TimeoutException:
            return JSONResponse(
                status_code=504,
                content={
                    "error": {
                        "message": "Gateway timeout - request took too long",
                        "type": "timeout_error"
                    }
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=502,
                content={
                    "error": {
                        "message": f"Bad gateway: {str(e)}",
                        "type": "proxy_error"
                    }
                }
            )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting Load Balancer on {host}:{port}")
    uvicorn.run(app, host=host, port=port)

