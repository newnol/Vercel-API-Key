# Config

Thư mục này chứa các file cấu hình.

## Files

- `key-list.json` - Danh sách Vercel API keys

## Cấu trúc key-list.json

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

**Lưu ý:** File này có thể chứa thông tin nhạy cảm. Đảm bảo không commit vào git nếu không cần thiết (đã được thêm vào .gitignore).

