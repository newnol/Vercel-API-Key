---
sidebar_position: 3
title: API Reference
---

# API Documentation

Detailed documentation of Load Balancer Server API endpoints.

## Base URL

```
http://localhost:8000
```

## Authentication

### Client API Keys

All requests to `/v1/*` require header:
```
Authorization: Bearer sk-lb-xxxxx
```

### Admin API

All requests to `/admin/*` require header:
```
Authorization: Bearer <ADMIN_SECRET>
```

## Health & Utility Endpoints

### GET /health

Basic health check endpoint.

**Authentication:** Not required

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-12-29T10:00:00.000000"
}
```

### GET /lb/health

Detailed health check with Vercel keys status.

**Authentication:** Not required

**Response:**
```json
{
  "status": "ok",
  "vercel_keys": [
    {
      "name": "Vercel 1",
      "balance": 4.03,
      "total_used": 15.97,
      "last_updated": "2025-12-29T..."
    }
  ],
  "total_balance": 31.51,
  "timestamp": "2025-12-29T..."
}
```

### POST /lb/refresh

Force refresh credit cache.

**Authentication:** Not required

**Response:**
```json
{
  "message": "Credit balance refreshed successfully",
  "total_balance": 31.51,
  "keys_count": 8
}
```

## Admin API Endpoints

### POST /admin/keys

Create new API key.

**Authentication:** Admin required

**Request Body:**
```json
{
  "name": "My App",
  "rate_limit": 60,
  "expires_in_days": 30
}
```

**Response:**
```json
{
  "message": "API key created successfully",
  "key": "sk-lb-xxxxx",
  "key_info": {
    "id": "uuid",
    "name": "My App",
    "rate_limit": 60,
    "expires_at": "2026-01-28T...",
    "created_at": "2025-12-29T..."
  },
  "warning": "Save this key now. It will not be shown again!"
}
```

### GET /admin/keys

List all API keys.

**Authentication:** Admin required

**Response:**
```json
{
  "keys": [
    {
      "id": "uuid",
      "name": "My App",
      "created_at": "2025-12-29T...",
      "expires_at": "2026-01-28T...",
      "rate_limit": 60,
      "is_active": true,
      "usage_count": 150
    }
  ]
}
```

### GET /admin/keys/\{key_id\}

Get key details and statistics.

**Authentication:** Admin required

**Response:**
```json
{
  "key_info": {
    "id": "uuid",
    "name": "My App",
    "created_at": "2025-12-29T...",
    "expires_at": "2026-01-28T...",
    "rate_limit": 60,
    "is_active": true
  },
  "stats": {
    "total_requests": 150,
    "total_tokens": 45000,
    "requests_by_endpoint": {
      "/v1/chat/completions": 140,
      "/v1/images/generations": 10
    },
    "requests_by_model": {
      "gpt-4o-mini": 140,
      "bfl/flux-2-pro": 10
    }
  }
}
```

### PATCH /admin/keys/\{key_id\}

Update API key.

**Authentication:** Admin required

**Request Body:**
```json
{
  "name": "Updated Name",
  "rate_limit": 100,
  "is_active": true,
  "expires_in_days": 60
}
```

**Response:**
```json
{
  "message": "API key updated successfully",
  "key_info": {
    "id": "uuid",
    "name": "Updated Name",
    "rate_limit": 100,
    "is_active": true,
    "expires_at": "2026-02-27T..."
  }
}
```

### DELETE /admin/keys/\{key_id\}

Delete API key.

**Authentication:** Admin required

**Response:**
```json
{
  "message": "API key deleted successfully"
}
```

## Proxy Endpoints

### ALL /v1/*

Proxy to Vercel AI Gateway with load balancing.

**Authentication:** Client API key required

**Supported endpoints:**
- `/v1/chat/completions` - Chat completions (including streaming)
- `/v1/images/generations` - Image generation
- `/v1/embeddings` - Text embeddings
- `/v1/models` - List available models
- And all other OpenAI-compatible endpoints

**Example (Chat Completions):**

Request:
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer sk-lb-xxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

Response: Standard OpenAI format

## Error Responses

### 401 Unauthorized

```json
{
  "error": {
    "message": "Invalid API key",
    "type": "authentication_error"
  }
}
```

### 429 Rate Limit Exceeded

```json
{
  "error": {
    "message": "Rate limit exceeded. Limit: 60 requests/minute",
    "type": "rate_limit_error"
  }
}
```

### 503 Service Unavailable

```json
{
  "error": {
    "message": "No available API keys with sufficient credit",
    "type": "service_unavailable"
  }
}
```

## Rate Limiting

Rate limiting uses **Sliding Window** algorithm:

- Counts requests in the last 60 seconds
- Returns 429 error if exceeds `rate_limit`
- Rate limit = 0 means unlimited

## Load Balancing

Server uses **Weighted Random Selection**:

1. Filters Vercel keys with balance > `MIN_CREDIT` (0.01)
2. Calculates total balance of all valid keys
3. Randomly selects a key with probability proportional to its balance
4. Keys with higher balance have higher probability of being selected

**Example:**
- Key A: $10 balance → ~50% probability
- Key B: $5 balance → ~25% probability
- Key C: $5 balance → ~25% probability

For complete API documentation and examples, visit the full documentation.
