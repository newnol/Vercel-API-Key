---
sidebar_position: 7
title: Deployment
---

# Docker Deployment Guide

## Requirements

- Docker and Docker Compose installed

## Method 1: Using Docker Compose (Recommended)

### Step 1: Configuration

1. Ensure `key-list.json` is created with your Vercel API keys:

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

2. Create `.env` file in root directory (or set environment variables):

```bash
ADMIN_SECRET=your-super-secret-admin-key-here
```

### Step 2: Build and Run

```bash
# Build and run container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down
```

### Step 3: Initialize Database

```bash
# Run init command inside container
docker-compose exec vercel-load-balancer python cli.py init
```
