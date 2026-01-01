# PocketBase Integration

Thư mục này chứa các file và tài liệu liên quan đến tích hợp PocketBase với project.

## Cấu trúc

- `test-pocketbase.py` - Script test kết nối và truy vấn dữ liệu từ PocketBase
- `README.md` - Tài liệu hướng dẫn sử dụng (file này)

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
Liệt kê tất cả records trong collection `Vercel_api_key`.

**Ví dụ:**
```python
result = test_list_records(page=1, per_page=10, use_bearer=True)
```

#### `test_get_record(record_id, expand, use_bearer)`
Lấy một record cụ thể theo ID.

**Ví dụ:**
```python
record = test_get_record('wbq31ghqzeguyy7', expand='relField1,relField2.subRelField', use_bearer=True)
```

#### `test_create_record(data)`
Tạo một record mới trong collection.

**Ví dụ:**
```python
new_record = test_create_record({
    'name': 'Vercel 3',
    'mail': 'example@gmail.com',
    'api_key': 'vck_xxxxx'
})
```

## API Endpoints

### List Records
```
GET /api/collections/Vercel_api_key/records?page=1&perPage=10
```

### Get Record by ID
```
GET /api/collections/Vercel_api_key/records/{record_id}?expand=relField1,relField2.subRelField
```

### Create Record
```
POST /api/collections/Vercel_api_key/records
Content-Type: application/json
Authorization: Bearer {token}

{
  "name": "Vercel 1",
  "mail": "example@gmail.com",
  "api_key": "vck_xxxxx"
}
```

## CURL Examples

### 1. Đăng nhập và lấy token
```bash
curl -X POST 'https://base.selfhost.io.vn/api/collections/_superusers/auth-with-password' \
     -H 'Content-Type: application/json' \
     -d '{
       "identity": "tantai13102005@gmail.com",
       "password": "ngotantai123"
     }'
```

### 2. List all records
```bash
curl -X GET 'https://base.selfhost.io.vn/api/collections/Vercel_api_key/records' \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer {YOUR_TOKEN}'
```

### 3. Get record by ID
```bash
curl -X GET 'https://base.selfhost.io.vn/api/collections/Vercel_api_key/records/{RECORD_ID}' \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer {YOUR_TOKEN}'
```

### 4. Create record
```bash
curl -X POST 'https://base.selfhost.io.vn/api/collections/Vercel_api_key/records' \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer {YOUR_TOKEN}' \
     -d '{
       "name": "Vercel 1",
       "mail": "example@gmail.com",
       "api_key": "vck_xxxxx"
     }'
```

## Lưu ý bảo mật

⚠️ **QUAN TRỌNG**: File `test-pocketbase.py` chứa thông tin đăng nhập nhạy cảm. 

- Không commit file này lên public repository
- Sử dụng environment variables hoặc file `.env` để lưu credentials
- Thêm vào `.gitignore` nếu cần

### Sử dụng Environment Variables (Khuyến nghị)

Tạo file `.env` trong thư mục `pocketbase/`:

```bash
POCKETBASE_URL=https://base.selfhost.io.vn
POCKETBASE_EMAIL=tantai13102005@gmail.com
POCKETBASE_PASSWORD=ngotantai123
```

Sau đó cập nhật script để đọc từ environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('POCKETBASE_URL', 'https://base.selfhost.io.vn')
ADMIN_EMAIL = os.getenv('POCKETBASE_EMAIL')
ADMIN_PASSWORD = os.getenv('POCKETBASE_PASSWORD')
```

## Dữ liệu hiện tại

Collection `Vercel_api_key` hiện có các trường:
- `id` - Record ID
- `name` - Tên của Vercel key
- `mail` - Email liên kết
- `api_key` - Vercel API key
- `created` - Thời gian tạo
- `updated` - Thời gian cập nhật

## Tài liệu tham khảo

- [PocketBase Official Documentation](https://pocketbase.io/docs/)
- [PocketBase API Collections](https://pocketbase.io/docs/api-collections/)
- [PocketBase Authentication](https://pocketbase.io/docs/api-authentication/)



