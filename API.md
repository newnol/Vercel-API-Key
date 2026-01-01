# API Documentation

Tài liệu chi tiết về các API endpoints của Load Balancer Server.

## Base URL

```
http://localhost:8000
```

## Authentication

### Client API Keys

Tất cả requests đến `/v1/*` yêu cầu header:
```
Authorization: Bearer sk-lb-xxxxx
```

### Admin API

Tất cả requests đến `/admin/*` yêu cầu header:
```
Authorization: Bearer <ADMIN_SECRET>
```

## Health & Utility Endpoints

### GET /health

Basic health check endpoint.

**Authentication:** Không cần

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-12-29T10:00:00.000000"
}
```

### GET /lb/health

Chi tiết health check với trạng thái các Vercel keys.

**Authentication:** Không cần

**Response:**
```json
{
  "status": "ok",
  "vercel_keys": [
    {
      "name": "Vercel 1",
      "balance": 4.03,
      "total_used": 15.97,
      "last_updated": "2025-12-29T10:00:00.000000"
    }
  ],
  "total_balance": 31.51,
  "timestamp": "2025-12-29T10:00:00.000000"
}
```

### POST /lb/refresh

Force refresh credit cache cho tất cả Vercel keys.

**Authentication:** Không cần

**Response:**
```json
{
  "message": "Credits refreshed",
  "keys_count": 9
}
```

## Admin API Endpoints

### POST /admin/keys

Tạo một API key mới.

**Authentication:** Admin Secret

**Request Body:**
```json
{
  "name": "My Application",
  "rate_limit": 60,
  "expires_in_days": 30
}
```

**Parameters:**
- `name` (required): Tên mô tả cho API key
- `rate_limit` (optional, default: 0): Giới hạn requests/phút (0 = unlimited)
- `expires_in_days` (optional): Số ngày hết hạn (null = không hết hạn)

**Response:**
```json
{
  "message": "API key created successfully",
  "key": "sk-lb-nzluPs0KFHPSk9PmBYl4heg29ZNJO_uT",
  "key_info": {
    "id": "cee24b30-1bc4-43aa-9088-cb4cef382d7a",
    "name": "My Application",
    "rate_limit": 60,
    "expires_at": "2026-01-28T09:59:12.318881",
    "created_at": "2025-12-29T09:59:12.318881"
  },
  "warning": "Save this key now. It will not be shown again!"
}
```

**⚠️ Lưu ý:** Key gốc chỉ hiển thị một lần trong response này.

### GET /admin/keys

Liệt kê tất cả API keys.

**Authentication:** Admin Secret

**Response:**
```json
{
  "keys": [
    {
      "id": "cee24b30-1bc4-43aa-9088-cb4cef382d7a",
      "name": "My Application",
      "rate_limit": 60,
      "is_active": true,
      "expires_at": "2026-01-28T09:59:12.318881",
      "created_at": "2025-12-29T09:59:12.318881"
    }
  ],
  "total": 1
}
```

### GET /admin/keys/{key_id}

Lấy chi tiết một API key kèm usage statistics.

**Authentication:** Admin Secret

**Response:**
```json
{
  "key_info": {
    "id": "cee24b30-1bc4-43aa-9088-cb4cef382d7a",
    "name": "My Application",
    "rate_limit": 60,
    "is_active": true,
    "expires_at": "2026-01-28T09:59:12.318881",
    "created_at": "2025-12-29T09:59:12.318881"
  },
  "stats": {
    "total_requests": 150,
    "total_tokens": 45000,
    "by_endpoint": {
      "/v1/chat/completions": 100,
      "/v1/images/generate": 50
    },
    "by_model": {
      "gpt-4o-mini": 80,
      "bfl/flux-2-pro": 50
    },
    "recent_requests": [
      {
        "timestamp": "2025-12-29T10:00:00.000000",
        "endpoint": "/v1/chat/completions",
        "tokens_used": 150,
        "model": "gpt-4o-mini"
      }
    ]
  }
}
```

### PATCH /admin/keys/{key_id}

Cập nhật một API key.

**Authentication:** Admin Secret

**Request Body:**
```json
{
  "name": "Updated Name",
  "rate_limit": 100,
  "is_active": true,
  "expires_in_days": 60
}
```

**Parameters:** (tất cả optional)
- `name`: Tên mới
- `rate_limit`: Rate limit mới
- `is_active`: Trạng thái active/inactive
- `expires_in_days`: Số ngày hết hạn từ hiện tại (null để xóa expiry)

**Response:**
```json
{
  "message": "Key updated successfully",
  "key_info": {
    "id": "cee24b30-1bc4-43aa-9088-cb4cef382d7a",
    "name": "Updated Name",
    "rate_limit": 100,
    "is_active": true,
    "expires_at": "2026-02-28T10:00:00.000000"
  }
}
```

### DELETE /admin/keys/{key_id}

Xóa một API key và tất cả usage logs liên quan.

**Authentication:** Admin Secret

**Response:**
```json
{
  "message": "Key deleted successfully",
  "key_id": "cee24b30-1bc4-43aa-9088-cb4cef382d7a"
}
```

## Proxy Endpoints

### ALL /v1/{path}

Proxy tất cả requests đến Vercel AI Gateway.

**Authentication:** Client API Key

**Behavior:**
- Tự động chọn Vercel key tốt nhất dựa trên balance
- Forward request đến `https://ai-gateway.vercel.sh/v1/{path}`
- Hỗ trợ streaming cho chat completions
- Log usage sau mỗi request thành công

**Supported Endpoints:**
- `/v1/chat/completions` - Chat completions
- `/v1/images/generate` - Image generation
- `/v1/embeddings` - Embeddings
- `/v1/models` - List models
- Tất cả endpoints khác của OpenAI API

**Example Request:**
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

**Example Response:**
```json
{
  "id": "gen_xxx",
  "object": "chat.completion",
  "created": 1767002427,
  "model": "openai/gpt-4o-mini",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 13,
    "completion_tokens": 8,
    "total_tokens": 21
  }
}
```

## Error Responses

Tất cả errors đều follow OpenAI error format:

```json
{
  "error": {
    "message": "Error description",
    "type": "error_type",
    "param": null,
    "code": null
  }
}
```

### Error Types

| Status Code | Error Type | Mô tả |
|-------------|------------|-------|
| 401 | `authentication_error` | Invalid hoặc missing API key |
| 429 | `rate_limit_error` | Vượt quá rate limit |
| 502 | `proxy_error` | Lỗi khi proxy đến Vercel |
| 503 | `server_error` | Không có Vercel key available |
| 504 | `timeout_error` | Request timeout |

### Example Error Responses

**Invalid API Key:**
```json
{
  "error": {
    "message": "Invalid or expired API key",
    "type": "authentication_error"
  }
}
```

**Rate Limit Exceeded:**
```json
{
  "error": {
    "message": "Rate limit exceeded. Limit: 60 requests/minute",
    "type": "rate_limit_error"
  }
}
```

**No Vercel Keys Available:**
```json
{
  "error": {
    "message": "No available Vercel API keys with sufficient credit",
    "type": "server_error"
  }
}
```

## Rate Limiting

Rate limiting sử dụng sliding window algorithm:
- Đếm requests trong 60 giây gần nhất
- Nếu vượt quá `rate_limit`, trả về 429
- Rate limit = 0 nghĩa là không giới hạn

## Usage Tracking

Mỗi request thành công sẽ được log với:
- `key_id`: ID của API key được sử dụng
- `timestamp`: Thời gian request
- `endpoint`: Endpoint được gọi
- `tokens_used`: Số tokens (nếu có trong response)
- `model`: Model được sử dụng (nếu có trong request)

## Load Balancing

Server tự động chọn Vercel key dựa trên:
1. Balance > `MIN_CREDIT` (0.01)
2. Weighted random selection theo balance
3. Key có balance cao hơn có xác suất được chọn cao hơn

Credit balance được cache trong 5 phút và tự động refresh định kỳ.



