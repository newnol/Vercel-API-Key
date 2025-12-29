# Vercel AI Gateway Load Balancer

Một FastAPI server hoạt động như reverse proxy cho Vercel AI Gateway với tính năng load balancing dựa trên credit balance và hệ thống xác thực API key.

## Tính năng

- ✅ **Load Balancing thông minh**: Tự động chọn Vercel API key dựa trên số credit còn lại (weighted random)
- ✅ **Xác thực API Key**: Client phải có API key hợp lệ mới có thể sử dụng
- ✅ **Rate Limiting**: Giới hạn số requests/phút cho mỗi API key
- ✅ **Usage Tracking**: Theo dõi số requests, tokens, models đã sử dụng
- ✅ **Expiry Date**: Hỗ trợ API key có thời hạn sử dụng
- ✅ **Admin API**: Quản lý keys qua REST API
- ✅ **CLI Tool**: Quản lý keys qua command line
- ✅ **100% OpenAI Compatible**: Hỗ trợ tất cả endpoints và streaming

## Cài đặt

### 1. Clone repository và cài đặt dependencies

```bash
# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cấu hình môi trường

Tạo file `.env` trong thư mục gốc:

```bash
# Admin secret để truy cập các endpoint /admin/*
# Generate một chuỗi ngẫu nhiên bảo mật, ví dụ: openssl rand -hex 32
ADMIN_SECRET=your-super-secret-admin-key-here

# Optional: Cấu hình server
HOST=0.0.0.0
PORT=8000
```

### 3. Chuẩn bị Vercel API Keys

Đảm bảo file `key-list.json` có cấu trúc như sau:

```json
{
    "keys": [
        {
            "name": "Vercel 1",
            "mail": "your-email@example.com",
            "api_key": "vck_xxxxx"
        }
    ]
}
```

### 4. Khởi tạo database

```bash
python cli.py init
```

### 5. Khởi động server

```bash
python server.py
```

Server sẽ chạy tại `http://localhost:8000` (hoặc port bạn đã cấu hình).

## Sử dụng CLI

### Tạo API key mới

```bash
python cli.py create-key --name "My Application" --rate-limit 60 --expires 30
```

**Options:**
- `--name` / `-n`: Tên của API key (bắt buộc)
- `--rate-limit` / `-r`: Giới hạn requests/phút (mặc định: 0 = unlimited)
- `--expires` / `-e`: Số ngày hết hạn (mặc định: không hết hạn)

**Ví dụ:**
```bash
# Tạo key không giới hạn rate limit, không hết hạn
python cli.py create-key --name "Production App"

# Tạo key với rate limit 100 req/min, hết hạn sau 90 ngày
python cli.py create-key --name "Test App" --rate-limit 100 --expires 90
```

**⚠️ Lưu ý:** API key sẽ chỉ hiển thị một lần khi tạo. Hãy lưu lại ngay!

### Liệt kê tất cả API keys

```bash
python cli.py list-keys
```

Output sẽ hiển thị bảng với các thông tin:
- ID
- Name
- Status (Active/Inactive/Expired)
- Rate Limit
- Expires date
- Created date

### Xem chi tiết một API key

```bash
python cli.py get-key <key-id>
```

### Xem thống kê sử dụng

```bash
python cli.py key-stats <key-id>
```

Hiển thị:
- Tổng số requests
- Tổng số tokens đã sử dụng
- Requests theo endpoint
- Requests theo model
- Recent requests

### Cập nhật API key

```bash
python cli.py update-key <key-id> --name "New Name" --rate-limit 120 --expires 60
```

**Options:**
- `--name` / `-n`: Đổi tên
- `--rate-limit` / `-r`: Cập nhật rate limit
- `--expires` / `-e`: Cập nhật expiry (số ngày từ hiện tại)
- `--activate`: Kích hoạt key
- `--deactivate`: Vô hiệu hóa key

### Xóa API key

```bash
python cli.py delete-key <key-id>

# Xóa không cần xác nhận
python cli.py delete-key <key-id> --yes
```

## Sử dụng Admin API

Tất cả các endpoint `/admin/*` yêu cầu header `Authorization: Bearer <ADMIN_SECRET>`.

### Tạo API key

```bash
curl -X POST http://localhost:8000/admin/keys \
  -H "Authorization: Bearer your-admin-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My App",
    "rate_limit": 60,
    "expires_in_days": 30
  }'
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

### Liệt kê tất cả keys

```bash
curl http://localhost:8000/admin/keys \
  -H "Authorization: Bearer your-admin-secret"
```

### Xem chi tiết key và stats

```bash
curl http://localhost:8000/admin/keys/<key-id> \
  -H "Authorization: Bearer your-admin-secret"
```

### Cập nhật key

```bash
curl -X PATCH http://localhost:8000/admin/keys/<key-id> \
  -H "Authorization: Bearer your-admin-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "rate_limit": 100,
    "is_active": true,
    "expires_in_days": 60
  }'
```

### Xóa key

```bash
curl -X DELETE http://localhost:8000/admin/keys/<key-id> \
  -H "Authorization: Bearer your-admin-secret"
```

## Tích hợp vào code

### Python với OpenAI SDK

```python
from openai import OpenAI

# Khởi tạo client với Load Balancer
client = OpenAI(
    api_key="sk-lb-your-api-key-here",  # API key từ CLI hoặc Admin API
    base_url="http://localhost:8000/v1",  # URL của Load Balancer
)

# Sử dụng như bình thường
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### JavaScript/TypeScript với OpenAI SDK

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'sk-lb-your-api-key-here',
  baseURL: 'http://localhost:8000/v1',
});

const completion = await client.chat.completions.create({
  model: 'gpt-4o-mini',
  messages: [{ role: 'user', content: 'Hello!' }],
});

console.log(completion.choices[0].message.content);
```

### Image Generation

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-lb-your-api-key-here",
    base_url="http://localhost:8000/v1",
)

# Generate image
response = client.images.generate(
    model="bfl/flux-2-pro",
    prompt="A majestic blue whale breaching the ocean surface at sunset",
    n=1,
    size="1024x1024"
)

print(response.data[0].url)
```

### Streaming (Chat Completions)

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-lb-your-api-key-here",
    base_url="http://localhost:8000/v1",
)

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## Health Check & Monitoring

### Kiểm tra trạng thái server

```bash
curl http://localhost:8000/health
```

### Kiểm tra trạng thái Vercel keys

```bash
curl http://localhost:8000/lb/health
```

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

### Force refresh credit cache

```bash
curl -X POST http://localhost:8000/lb/refresh
```

## Cấu trúc Database

Server sử dụng SQLite database (`lb_database.db`) với 2 bảng chính:

### `api_keys`
- `id`: UUID của key
- `key_hash`: SHA256 hash của API key
- `name`: Tên mô tả
- `created_at`: Thời gian tạo
- `expires_at`: Thời gian hết hạn (NULL = không hết hạn)
- `rate_limit`: Giới hạn requests/phút (0 = unlimited)
- `is_active`: Trạng thái active/inactive

### `usage_logs`
- `id`: Auto increment ID
- `key_id`: Foreign key đến `api_keys.id`
- `timestamp`: Thời gian request
- `endpoint`: Endpoint được gọi (ví dụ: `/v1/chat/completions`)
- `tokens_used`: Số tokens đã sử dụng (nullable)
- `model`: Model được sử dụng (nullable)

## Load Balancing Algorithm

Server sử dụng **Weighted Random Selection**:

1. Lọc các Vercel keys có balance > `MIN_CREDIT` (0.01)
2. Tính tổng balance của tất cả keys hợp lệ
3. Chọn ngẫu nhiên một key với xác suất tỷ lệ với balance của nó
4. Key có balance cao hơn sẽ có xác suất được chọn cao hơn

**Ví dụ:**
- Key A: $10 balance → xác suất ~50%
- Key B: $5 balance → xác suất ~25%
- Key C: $5 balance → xác suất ~25%

## Rate Limiting

Rate limiting sử dụng **Sliding Window** algorithm:

- Đếm số requests trong 60 giây gần nhất
- Nếu vượt quá `rate_limit`, trả về lỗi 429
- Rate limit = 0 nghĩa là không giới hạn

**Error response khi vượt rate limit:**
```json
{
  "error": {
    "message": "Rate limit exceeded. Limit: 60 requests/minute",
    "type": "rate_limit_error"
  }
}
```

## Security Best Practices

1. **Bảo vệ ADMIN_SECRET**: 
   - Không commit vào git
   - Sử dụng biến môi trường
   - Generate một chuỗi ngẫu nhiên mạnh

2. **API Key Storage**:
   - Chỉ lưu hash trong database, không lưu key gốc
   - Key gốc chỉ hiển thị một lần khi tạo

3. **Rate Limiting**:
   - Đặt rate limit phù hợp với use case
   - Monitor usage để phát hiện abuse

4. **Expiry Dates**:
   - Đặt expiry date cho các key test/development
   - Rotate keys định kỳ cho production

## Troubleshooting

### Server không start được

**Lỗi:** `ADMIN_SECRET environment variable is not set`

**Giải pháp:** Thêm `ADMIN_SECRET` vào file `.env`

### Không có Vercel key nào available

**Lỗi:** `No available API keys with sufficient credit`

**Giải pháp:**
- Kiểm tra file `key-list.json` có đúng format không
- Kiểm tra các Vercel keys còn credit không: `curl http://localhost:8000/lb/health`
- Refresh credit cache: `curl -X POST http://localhost:8000/lb/refresh`

### API key không hoạt động

**Kiểm tra:**
1. Key có active không: `python cli.py get-key <key-id>`
2. Key có hết hạn không
3. Rate limit có bị vượt không
4. Format header đúng: `Authorization: Bearer sk-lb-xxx`

### Database errors

**Giải pháp:** Khởi tạo lại database:
```bash
rm lb_database.db
python cli.py init
```

## API Endpoints Summary

| Endpoint | Method | Auth | Mô tả |
|----------|--------|------|-------|
| `/health` | GET | None | Basic health check |
| `/lb/health` | GET | None | Detailed health với Vercel key status |
| `/lb/refresh` | POST | None | Force refresh credit cache |
| `/admin/keys` | POST | Admin | Tạo API key mới |
| `/admin/keys` | GET | Admin | List tất cả keys |
| `/admin/keys/{id}` | GET | Admin | Chi tiết key + stats |
| `/admin/keys/{id}` | PATCH | Admin | Update key |
| `/admin/keys/{id}` | DELETE | Admin | Xóa key |
| `/v1/*` | ALL | Client | Proxy đến Vercel AI Gateway |

## License

MIT License

## Support

Nếu gặp vấn đề, hãy kiểm tra:
1. Logs của server
2. Health check endpoint
3. Database có được khởi tạo đúng không
4. File `key-list.json` có đúng format không

