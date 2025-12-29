# Cấu trúc Project

## Tổng quan

```
Vercel-API-Key/
├── config/              # Cấu hình
│   ├── key-list.json           # Vercel API keys (không commit vào git)
│   └── key-list.example.json   # Template mẫu
├── data/                # Dữ liệu
│   ├── lb_database.db          # SQLite database
│   └── output/                 # Output files (images, etc.)
├── scripts/             # Utility scripts
│   ├── start-server.sh         # Script khởi động server
│   ├── generate-image.py       # Generate images
│   └── track-credit.py         # Track credit usage
├── tests/               # Test files
│   ├── test-api-key.py         # Test API key
│   ├── test-pocketbase-connection.py  # Test PocketBase
│   └── test-pocketbase.py      # PocketBase test script
├── pocketbase/          # PocketBase utilities (optional)
├── server.py            # FastAPI server chính
├── cli.py               # CLI tool
├── auth.py              # Authentication middleware
├── database.py          # Database operations
├── pocketbase_client.py # PocketBase client (optional)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image
├── docker-compose.yml   # Docker Compose config
└── README.md            # Documentation chính
```

## Mô tả các thư mục

### `config/`
Chứa các file cấu hình:
- `key-list.json`: Danh sách Vercel API keys (không được commit vào git)
- `key-list.example.json`: Template mẫu để tham khảo

### `data/`
Chứa dữ liệu runtime:
- `lb_database.db`: SQLite database cho API keys và usage logs
- `output/`: Các file output (images, logs, etc.)

### `scripts/`
Các utility scripts:
- `start-server.sh`: Script để khởi động server với kiểm tra cấu hình
- `generate-image.py`: Script để generate images
- `track-credit.py`: Script để track credit usage

### `tests/`
Các file test:
- `test-api-key.py`: Test API key với OpenAI client
- `test-pocketbase-connection.py`: Test kết nối PocketBase
- `test-pocketbase.py`: Script test PocketBase chi tiết

## File quan trọng

### Core Files
- `server.py`: FastAPI server chính, xử lý proxy requests
- `cli.py`: Command-line interface để quản lý API keys
- `auth.py`: Authentication middleware
- `database.py`: Database operations với SQLite

### Configuration
- `.env`: Environment variables (không commit vào git)
- `config/key-list.json`: Vercel API keys (không commit vào git)
- `requirements.txt`: Python dependencies

### Docker
- `Dockerfile`: Docker image definition
- `docker-compose.yml`: Docker Compose configuration
- `.dockerignore`: Files to exclude from Docker build

## Git

Project đã được khởi tạo với git. Các file sau được loại trừ khỏi git:

- `venv/` - Virtual environment
- `__pycache__/` - Python cache
- `*.db`, `*.sqlite` - Database files
- `config/key-list.json` - Sensitive API keys
- `.env` - Environment variables
- `data/output/` - Output files

## Cách sử dụng

1. **Setup lần đầu:**
   ```bash
   # Copy example config
   cp config/key-list.example.json config/key-list.json
   # Edit config/key-list.json với API keys thực tế
   
   # Tạo .env file
   echo "ADMIN_SECRET=your-secret" > .env
   ```

2. **Khởi động server:**
   ```bash
   ./scripts/start-server.sh
   # hoặc
   python server.py
   ```

3. **Chạy tests:**
   ```bash
   python tests/test-api-key.py
   ```

4. **Docker:**
   ```bash
   docker-compose up -d
   ```

