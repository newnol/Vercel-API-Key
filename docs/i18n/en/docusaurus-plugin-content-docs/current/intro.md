---
sidebar_position: 1
title: Introduction
---

# Vercel AI Gateway Load Balancer

A FastAPI server that acts as a reverse proxy for Vercel AI Gateway with intelligent load balancing based on credit balance and API key authentication system.

## 📚 Documentation

- **[Introduction](intro)** - Main documentation (this page)
- **[Quick Start](quickstart)** - 5-minute setup guide
- **[API Reference](api)** - API endpoints details
- **[Contributing](contributing)** - Contributing guidelines
- **[Security Cleanup](security)** - Remove secrets from Git history
- **[Project Structure](project-structure)** - Project structure

## Features

- ✅ **Smart Load Balancing**: Automatically select Vercel API keys based on remaining credit balance (weighted random)
- ✅ **API Key Authentication**: Clients must have valid API keys to use the service
- ✅ **Rate Limiting**: Limit requests/minute for each API key
- ✅ **Usage Tracking**: Track requests, tokens, and models used
- ✅ **Expiry Date**: Support API keys with expiration dates
- ✅ **Admin API**: Manage keys via REST API
- ✅ **CLI Tool**: Manage keys via command line
- ✅ **100% OpenAI Compatible**: Support all endpoints and streaming
- 🔒 **Security**: Pre-commit hooks with Gitleaks to prevent secrets from being committed
- 🔒 **Best Practices**: Template files and security documentation

## Installation

### 1. Clone repository and install dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks (recommended)
pip install pre-commit
pre-commit install
```

### 2. Environment Configuration

Create `.env` file in root directory:

```bash
# Copy from template
cp .env.example .env

# Then edit .env with your actual information
```

Contents of `.env` file:

```bash
# Admin secret to access /admin/* endpoints
# Generate a secure random string, e.g.: openssl rand -hex 32
ADMIN_SECRET=your-super-secret-admin-key-here

# Optional: Server configuration
HOST=0.0.0.0
PORT=8000

# PocketBase Configuration (recommended)
USE_POCKETBASE=true
POCKETBASE_URL=https://base.selfhost.io.vn
POCKETBASE_COLLECTION=Vercel_api_key
POCKETBASE_EMAIL=your-email@example.com
POCKETBASE_PASSWORD=your-password
```

### 3. Prepare Vercel API Keys

#### Method 1: PocketBase (Recommended)

Server will automatically fetch keys from PocketBase collection. Collection structure requires these fields:
- `name`: Key name
- `api_key`: Vercel API key (vck_xxxxx)
- `mail`: Email (optional)

Test PocketBase connection:
```bash
python tests/test-pocketbase.py
```

#### Method 2: JSON File (Fallback)

If not using PocketBase or PocketBase fails, server will fallback to `config/key-list.json`:

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

To disable PocketBase and only use JSON file:
```bash
USE_POCKETBASE=false
```

### 4. Initialize Database

```bash
python cli.py init
```

### 5. Start Server

```bash
python server.py
```

Server will run at `http://localhost:8000` (or your configured port).

## Using CLI

### Create New API Key

```bash
python cli.py create-key --name "My Application"
```

**Options:**
- `--name` / `-n`: API key name (required)
- `--rate-limit` / `-r`: Requests/minute limit (default: 0 = unlimited)
- `--expires` / `-e`: Days until expiration (default: no expiration)

**Examples:**
```bash
# Create key with no rate limit, no expiration
python cli.py create-key --name "Production App"

# Create key with 100 req/min rate limit, expires in 90 days
python cli.py create-key --name "Test App" --rate-limit 100 --expires 90
```

**⚠️ Note:** API key will only be displayed once when created. Save it immediately!

### List All API Keys

```bash
python cli.py list-keys
```

Output will display table with information:
- ID
- Name
- Status (Active/Inactive/Expired)
- Rate Limit
- Expires date
- Created date

### View API Key Details

```bash
python cli.py get-key <key-id>
```

### View Usage Statistics

```bash
python cli.py key-stats <key-id>
```

Displays:
- Total requests
- Total tokens used
- Requests by endpoint
- Requests by model
- Recent requests

For complete documentation, see the full documentation pages.
