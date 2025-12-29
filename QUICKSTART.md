# Quick Start Guide

Hướng dẫn nhanh để bắt đầu sử dụng Vercel AI Gateway Load Balancer trong 5 phút.

## Bước 1: Cài đặt

```bash
# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt dependencies
pip3 install -r requirements.txt
```

## Bước 2: Cấu hình

Tạo file `.env`:

```bash
ADMIN_SECRET=your-secret-here-change-this
```

Đảm bảo file `key-list.json` đã được tạo với các Vercel API keys của bạn.

## Bước 3: Khởi tạo Database

```bash
python cli.py init
```

## Bước 4: Khởi động Server

```bash
python server.py
```

Server sẽ chạy tại `http://localhost:8000`

## Bước 5: Tạo API Key cho Client

```bash
python3 cli.py create-key --name "My App" --rate-limit 60
```

**Lưu lại API key được hiển thị!** (format: `sk-lb-xxxxx`)

## Bước 6: Sử dụng trong Code

### Python

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-lb-your-key-here",  # Key từ bước 5
    base_url="http://localhost:8000/v1",
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

### JavaScript/TypeScript

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'sk-lb-your-key-here',
  baseURL: 'http://localhost:8000/v1',
});

const completion = await client.chat.completions.create({
  model: 'gpt-4o-mini',
  messages: [{ role: 'user', content: 'Hello!' }],
});

console.log(completion.choices[0].message.content);
```

## Kiểm tra Server

```bash
# Health check
curl http://localhost:8000/health

# Xem Vercel keys status
curl http://localhost:8000/lb/health
```

## Các lệnh CLI thường dùng

```bash
# List tất cả keys
python cli.py list-keys

# Xem stats của một key
python cli.py key-stats <key-id>

# Xóa key
python cli.py delete-key <key-id>
```

## Xem thêm

Xem file [README.md](README.md) để biết chi tiết đầy đủ.

