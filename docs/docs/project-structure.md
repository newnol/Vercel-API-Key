---
sidebar_position: 6
title: Project Structure
---

# Cấu trúc Project

## Tổng quan

```
Vercel-API-Key/
├── config/              # Cấu hình
│   ├── key-list.json           # Vercel API keys (không commit vào git)
│   ├── key-list.example.json   # Template mẫu
│   └── README.md               # Config documentation
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
│   ├── test-pocketbase.py      # PocketBase test script
│   ├── .env                    # Test environment (gitignored)
│   └── .env.example            # Test env template
├── pocketbase/          # PocketBase utilities (optional)
├── server.py            # FastAPI server chính
├── cli.py               # CLI tool
├── auth.py              # Authentication middleware
├── database.py          # Database operations
├── pocketbase_client.py # PocketBase client (optional)
├── .env                 # Environment variables (gitignored)
├── .env.example         # Environment template
├── .gitignore           # Git ignore rules
├── .pre-commit-config.yaml  # Pre-commit hooks config
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image
├── docker-compose.yml   # Docker Compose config
├── README.md            # Documentation chính
├── QUICKSTART.md        # Quick start guide
├── API.md               # API documentation
├── CONTRIBUTING.md      # Contributing guidelines
├── SECURITY_CLEANUP.md  # Security cleanup guide
└── PROJECT_STRUCTURE.md # This file
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
- `.env.example`: Template cho .env file
- `config/key-list.json`: Vercel API keys (không commit vào git)
- `requirements.txt`: Python dependencies

### Security
- `.gitignore`: Danh sách files không commit vào git
- `.pre-commit-config.yaml`: Cấu hình pre-commit hooks với Gitleaks
- `SECURITY_CLEANUP.md`: Hướng dẫn xóa secrets khỏi Git history
- `CONTRIBUTING.md`: Hướng dẫn contribute với security guidelines

### Docker
- `Dockerfile`: Docker image definition
- `docker-compose.yml`: Docker Compose configuration
- `.dockerignore`: Files to exclude from Docker build

## Git

Project đã được khởi tạo với git và security measures. Các file sau được loại trừ khỏi git:

- `venv/` - Virtual environment
- `__pycache__/` - Python cache
- `*.db`, `*.sqlite` - Database files
- `config/key-list.json` - Sensitive API keys
- `.env`, `tests/.env` - Environment variables
- `data/output/` - Output files
- `gitleaks-report.json` - Gitleaks scan reports

### 🔒 Security Features

1. **Pre-commit Hooks**: Tự động quét secrets với Gitleaks trước mỗi commit
2. **Gitignore**: Tất cả sensitive files đã được gitignore
3. **Templates**: `.env.example` và `key-list.example.json` để reference

## Cách sử dụng

1. **Setup lần đầu:**
   ```bash
   # Copy example configs
   cp .env.example .env
   cp config/key-list.example.json config/key-list.json

   # Edit với thông tin thực tế
   # .env - Thêm ADMIN_SECRET
   # config/key-list.json - Thêm Vercel API keys

   # Cài đặt pre-commit hooks
   pip install pre-commit
   pre-commit install
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
