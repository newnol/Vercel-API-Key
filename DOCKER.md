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

### Bước 4: Tạo API key cho client

```bash
docker-compose exec vercel-load-balancer python cli.py create-key --name "My App" --rate-limit 60
```

## Cách 2: Sử dụng Docker trực tiếp

### Bước 1: Build image

```bash
docker build -t vercel-load-balancer .
```

### Bước 2: Chạy container

```bash
docker run -d \
  --name vercel-load-balancer \
  -p 8000:8000 \
  -e ADMIN_SECRET=your-super-secret-admin-key-here \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/key-list.json:/app/key-list.json:ro \
  vercel-load-balancer
```

### Bước 3: Khởi tạo database và tạo key

```bash
# Init database
docker exec vercel-load-balancer python cli.py init

# Tạo API key
docker exec vercel-load-balancer python cli.py create-key --name "My App" --rate-limit 60
```

## Quản lý Container

### Xem logs

```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f vercel-load-balancer
```

### Dừng/Start container

```bash
# Docker Compose
docker-compose stop
docker-compose start
docker-compose restart

# Docker
docker stop vercel-load-balancer
docker start vercel-load-balancer
docker restart vercel-load-balancer
```

### Xóa container

```bash
# Docker Compose
docker-compose down

# Docker
docker rm -f vercel-load-balancer
```

## Cấu trúc Volume

- `./data` - Chứa database SQLite (`lb_database.db`)
- `./key-list.json` - File chứa Vercel API keys (read-only)

## Environment Variables

- `ADMIN_SECRET` (bắt buộc): Secret key để truy cập admin API
- `PORT` (tùy chọn): Port để chạy server (mặc định: 8000)
- `HOST` (tùy chọn): Host để bind (mặc định: 0.0.0.0)
- `DATABASE_PATH` (tùy chọn): Đường dẫn database (mặc định: lb_database.db)

## Troubleshooting

### Kiểm tra container có chạy không

```bash
docker ps | grep vercel-load-balancer
```

### Kiểm tra health check

```bash
# Từ host
curl http://localhost:8000/health

# Từ trong container
docker exec vercel-load-balancer python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read())"
```

### Xem logs lỗi

```bash
docker-compose logs --tail=100 vercel-load-balancer
```

### Vào trong container để debug

```bash
docker exec -it vercel-load-balancer /bin/bash
```

## Deploy lên Production

### 1. Build image cho production

```bash
docker build -t your-registry/vercel-load-balancer:latest .
```

### 2. Push lên registry (nếu cần)

```bash
docker push your-registry/vercel-load-balancer:latest
```

### 3. Chạy trên server

```bash
# Pull image
docker pull your-registry/vercel-load-balancer:latest

# Run với production config
docker run -d \
  --name vercel-load-balancer \
  -p 8000:8000 \
  -e ADMIN_SECRET=your-production-secret \
  -v /path/to/data:/app/data \
  -v /path/to/key-list.json:/app/key-list.json:ro \
  --restart unless-stopped \
  your-registry/vercel-load-balancer:latest
```

## Lưu ý bảo mật

1. **Đổi ADMIN_SECRET**: Luôn đặt một secret key mạnh cho production
2. **Backup database**: Thường xuyên backup thư mục `data/`
3. **Firewall**: Chỉ expose port 8000 nếu cần thiết
4. **HTTPS**: Sử dụng reverse proxy (nginx/traefik) với SSL/TLS cho production

