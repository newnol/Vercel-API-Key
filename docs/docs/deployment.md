---
sidebar_position: 7
title: Deployment
---

# Hướng dẫn chạy với Docker

## Yêu cầu

- Docker và Docker Compose đã được cài đặt

## Cách 1: Sử dụng Docker Compose (Khuyến nghị)

### Bước 1: Chuẩn bị file cấu hình

1. Đảm bảo file `key-list.json` đã được tạo với các Vercel API keys của bạn:

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

2. Tạo file `.env` trong thư mục gốc (hoặc set biến môi trường):

```bash
ADMIN_SECRET=your-super-secret-admin-key-here
```

### Bước 2: Build và chạy

```bash
# Build và chạy container
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng container
docker-compose down
```

### Bước 3: Khởi tạo database

```bash
# Chạy lệnh init trong container
docker-compose exec vercel-load-balancer python cli.py init
```
