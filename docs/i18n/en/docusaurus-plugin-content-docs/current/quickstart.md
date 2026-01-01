---
sidebar_position: 2
title: Quick Start
---

# Quick Start Guide

Quick guide to get started with Vercel AI Gateway Load Balancer in 5 minutes.

## Step 1: Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Install pre-commit hooks (security)
pip3 install pre-commit
pre-commit install
```

## Step 2: Configuration

Create `.env` file from template:

```bash
# Copy from example
cp .env.example .env

# Generate strong ADMIN_SECRET
echo "ADMIN_SECRET=$(openssl rand -hex 32)" >> .env
```

Ensure `config/key-list.json` is created with your Vercel API keys (or use PocketBase).

## Step 3: Initialize Database

```bash
python cli.py init
```

## Step 4: Start Server

```bash
python server.py
```

Server will run at `http://localhost:8000`

## Step 5: Create API Key for Client

```bash
python3 cli.py create-key --name "My App" --rate-limit 60
```

**Save the displayed API key!** (format: `sk-lb-xxxxx`)

## Step 6: Use in Code

### Python

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-lb-your-key-here",  # Key from step 5
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

## Check Server

```bash
# Health check
curl http://localhost:8000/health

# View Vercel keys status
curl http://localhost:8000/lb/health
```

## Common CLI Commands

```bash
# List all keys
python cli.py list-keys

# View key stats
python cli.py key-stats <key-id>

# Delete key
python cli.py delete-key <key-id>
```

## 🔒 Security Tips

- ✅ Pre-commit hooks will automatically scan for secrets
- ✅ `.env` file is gitignored - no worry about accidental commits
- ✅ Always use strong ADMIN_SECRET (generated with openssl)
- ⚠️ Don't commit `config/key-list.json` to git
- 📖 Read [Security Cleanup Guide](security) if needed

## See More

See [Full Documentation](intro) for complete details.
