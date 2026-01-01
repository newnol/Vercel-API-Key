---
sidebar_position: 6
title: Project Structure
---

# Project Structure

## Overview

```
Vercel-API-Key/
├── config/              # Configuration
│   ├── key-list.json           # Vercel API keys (not committed to git)
│   ├── key-list.example.json   # Example template
│   └── README.md               # Config documentation
├── data/                # Data
│   ├── lb_database.db          # SQLite database
│   └── output/                 # Output files (images, etc.)
├── scripts/             # Utility scripts
│   ├── start-server.sh         # Server startup script
│   ├── generate-image.py       # Generate images
│   └── track-credit.py         # Track credit usage
├── tests/               # Test files
│   ├── test-api-key.py         # Test API key
│   ├── test-pocketbase-connection.py  # Test PocketBase
│   ├── test-pocketbase.py      # PocketBase test script
│   ├── .env                    # Test environment (gitignored)
│   └── .env.example            # Test env template
├── pocketbase/          # PocketBase utilities (optional)
├── docs/                # Documentation website
│   ├── docs/                   # Markdown documentation
│   ├── src/                    # React components
│   └── static/                 # Static assets
├── server.py            # Main FastAPI server
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
├── README.md            # Main documentation
├── QUICKSTART.md        # Quick start guide
├── API.md               # API documentation
├── CONTRIBUTING.md      # Contributing guidelines
├── SECURITY_CLEANUP.md  # Security cleanup guide
└── PROJECT_STRUCTURE.md # This file
```

## Directory Description

### `config/`
Contains configuration files:
- `key-list.json`: List of Vercel API keys (not committed to git)
- `key-list.example.json`: Example template for reference

### `data/`
Contains runtime data:
- `lb_database.db`: SQLite database for API keys and usage logs
- `output/`: Output files (images, logs, etc.)

### `scripts/`
Utility scripts:
- `start-server.sh`: Script to start server with configuration check
- `generate-image.py`: Script to generate images
- `track-credit.py`: Script to track credit usage

### `tests/`
Test files:
- `test-api-key.py`: Test API key with OpenAI client
- `test-pocketbase-connection.py`: Test PocketBase connection
- `test-pocketbase.py`: Detailed PocketBase test script

### `docs/`
Documentation website (Docusaurus):
- `docs/`: Markdown documentation files
- `src/`: React components and custom pages
- `static/`: Static assets (images, files)
- `i18n/`: Internationalization files

## Important Files

### Core Files
- `server.py`: Main FastAPI server, handles proxy requests
- `cli.py`: Command-line interface for managing API keys
- `auth.py`: Authentication middleware
- `database.py`: Database operations with SQLite

### Configuration
- `.env`: Environment variables (not committed to git)
- `.env.example`: Template for .env file
- `config/key-list.json`: Vercel API keys (not committed to git)
- `requirements.txt`: Python dependencies

### Security
- `.gitignore`: List of files not committed to git
- `.pre-commit-config.yaml`: Pre-commit hooks configuration with Gitleaks
- `SECURITY_CLEANUP.md`: Guide to remove secrets from Git history
- `CONTRIBUTING.md`: Contributing guidelines with security guidelines

### Docker
- `Dockerfile`: Docker image definition
- `docker-compose.yml`: Docker Compose configuration
- `.dockerignore`: Files to exclude from Docker build

## Git

Project has been initialized with git and security measures. Following files are excluded from git:

- `venv/` - Virtual environment
- `__pycache__/` - Python cache
- `*.db`, `*.sqlite` - Database files
- `config/key-list.json` - Sensitive API keys
- `.env`, `tests/.env` - Environment variables
- `data/output/` - Output files
- `gitleaks-report.json` - Gitleaks scan reports
- `docs/node_modules/`, `docs/build/` - Docusaurus build files

### 🔒 Security Features

1. **Pre-commit Hooks**: Automatically scan secrets with Gitleaks before each commit
2. **Gitignore**: All sensitive files are gitignored
3. **Templates**: `.env.example` and `key-list.example.json` for reference

## Usage

1. **Initial Setup:**
   ```bash
   # Copy example configs
   cp .env.example .env
   cp config/key-list.example.json config/key-list.json

   # Edit with actual information
   # .env - Add ADMIN_SECRET
   # config/key-list.json - Add Vercel API keys

   # Install pre-commit hooks
   pip install pre-commit
   pre-commit install
   ```

2. **Start Server:**
   ```bash
   ./scripts/start-server.sh
   # or
   python server.py
   ```

3. **Development:**
   ```bash
   # Run tests
   python -m pytest tests/

   # Start docs site
   cd docs && npm start
   ```

## Documentation Website

The `docs/` directory contains a Docusaurus-powered documentation website with:
- Multiple language support (Vietnamese, English)
- Interactive examples
- API reference
- Automatic deployment to GitHub Pages

See [docs/README.md](https://github.com/newnol/Vercel-API-Key/blob/main/docs/README.md) for more information.
