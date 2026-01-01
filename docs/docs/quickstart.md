---
sidebar_position: 2
title: Quick Start
---

# Quick Start Guide

Hướng dẫn nhanh để bắt đầu sử dụng Vercel AI Gateway Load Balancer trong 5 phút.

## Bước 1: Cài đặt

```bash
# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt dependencies
pip3 install -r requirements.txt

# Cài đặt pre-commit hooks (bảo mật)
pip3 install pre-commit
pre-commit install
```

## Bước 2: Cấu hình

Tạo file `.env` từ template:

```bash
# Copy từ example
cp .env.example .env

# Generate ADMIN_SECRET mạnh
echo "ADMIN_SECRET=$(openssl rand -hex 32)" >> .env
```

Đảm bảo file `config/key-list.json` đã được tạo với các Vercel API keys của bạn (hoặc dùng PocketBase).

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

## 🔒 Security Tips

- ✅ Pre-commit hooks đã được cài đặt sẽ tự động quét secrets
- ✅ File `.env` đã được gitignore - không lo bị commit nhầm
- ✅ Luôn dùng ADMIN_SECRET mạnh (generated bằng openssl)
- ⚠️ Không commit file `config/key-list.json` vào git
- 📖 Đọc [Security Cleanup Guide](security) nếu cần

## Xem thêm

Xem [Full Documentation](intro) để biết chi tiết đầy đủ.
