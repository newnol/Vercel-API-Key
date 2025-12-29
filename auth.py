"""
Authentication and rate limiting middleware for the Load Balancer.
"""

import os
from typing import Optional, Callable
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from database import validate_key, log_usage, get_request_count_in_window, APIKey


def get_admin_secret() -> str:
    """Get the admin secret from environment."""
    secret = os.getenv("ADMIN_SECRET")
    if not secret:
        raise ValueError("ADMIN_SECRET environment variable is not set")
    return secret


def extract_api_key(request: Request) -> Optional[str]:
    """Extract API key from Authorization header."""
    auth_header = request.headers.get("Authorization", "")
    
    if auth_header.startswith("Bearer "):
        return auth_header[7:]  # Remove "Bearer " prefix
    
    return None


def is_admin_path(path: str) -> bool:
    """Check if the path is an admin endpoint."""
    return path.startswith("/admin/")


def is_health_path(path: str) -> bool:
    """Check if the path is a health/utility endpoint."""
    return path in ["/lb/health", "/lb/refresh", "/health", "/docs", "/openapi.json", "/redoc"]


async def verify_admin_auth(request: Request) -> bool:
    """Verify admin authentication."""
    api_key = extract_api_key(request)
    if not api_key:
        return False
    
    try:
        admin_secret = get_admin_secret()
        return api_key == admin_secret
    except ValueError:
        return False


async def verify_client_auth(request: Request) -> tuple[bool, Optional[APIKey], Optional[str]]:
    """
    Verify client API key authentication.
    Returns (is_valid, api_key_object, error_message)
    """
    raw_key = extract_api_key(request)
    
    if not raw_key:
        return False, None, "Missing API key. Use Authorization: Bearer <your-api-key>"
    
    # Validate the key
    api_key = await validate_key(raw_key)
    
    if not api_key:
        return False, None, "Invalid or expired API key"
    
    # Check rate limit
    if api_key.rate_limit > 0:
        request_count = await get_request_count_in_window(api_key.id, window_seconds=60)
        if request_count >= api_key.rate_limit:
            return False, api_key, f"Rate limit exceeded. Limit: {api_key.rate_limit} requests/minute"
    
    return True, api_key, None


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that handles authentication for all requests.
    - Admin endpoints require ADMIN_SECRET
    - Proxy endpoints require valid client API key
    - Health endpoints are public
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        path = request.url.path
        
        # Allow health/utility endpoints without auth
        if is_health_path(path):
            return await call_next(request)
        
        # Admin endpoints require admin secret
        if is_admin_path(path):
            if not await verify_admin_auth(request):
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": {
                            "message": "Invalid or missing admin credentials",
                            "type": "authentication_error"
                        }
                    }
                )
            return await call_next(request)
        
        # All other endpoints require client API key
        is_valid, api_key, error_message = await verify_client_auth(request)
        
        if not is_valid:
            status_code = 429 if error_message and "Rate limit" in error_message else 401
            return JSONResponse(
                status_code=status_code,
                content={
                    "error": {
                        "message": error_message,
                        "type": "authentication_error" if status_code == 401 else "rate_limit_error"
                    }
                }
            )
        
        # Store API key info in request state for later use
        request.state.api_key = api_key
        
        # Call the actual endpoint
        response = await call_next(request)
        
        # Log usage after successful request (async, non-blocking)
        if api_key and response.status_code < 400:
            # Extract model from request body if available
            model = None
            try:
                # We can't easily access request body in middleware after it's consumed
                # So we'll log without model info here, or use a different approach
                pass
            except:
                pass
            
            await log_usage(
                key_id=api_key.id,
                endpoint=path,
                model=model
            )
        
        return response


def create_openai_error_response(message: str, error_type: str, status_code: int) -> JSONResponse:
    """Create an OpenAI-compatible error response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "message": message,
                "type": error_type,
                "param": None,
                "code": None
            }
        }
    )

