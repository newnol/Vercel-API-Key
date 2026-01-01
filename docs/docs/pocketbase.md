---
sidebar_position: 8
title: PocketBase Integration
---

# PocketBase Integration

Tài liệu hướng dẫn tích hợp PocketBase với project.

## Cấu hình

### PocketBase Server
- **Base URL**: `https://base.selfhost.io.vn`
- **Collection**: `Vercel_api_key`

### Authentication

Script sử dụng superuser authentication để truy cập PocketBase:

- **Endpoint**: `/api/collections/_superusers/auth-with-password`
- **Method**: POST
- **Body**:
  ```json
  {
    "identity": "your-email@example.com",
    "password": "your-password"
  }
  ```

## Sử dụng

### 1. Chạy script test

```bash
# Từ thư mục gốc của project
cd pocketbase
python test-pocketbase.py

# Hoặc từ thư mục gốc
python pocketbase/test-pocketbase.py
```

### 2. Các chức năng

Script `test-pocketbase.py` cung cấp các hàm sau:

#### `admin_login()`
Đăng nhập với tài khoản superuser và lấy authentication token.

#### `test_list_records(page, per_page, expand, use_bearer)`
Lấy danh sách records từ collection.
