#!/bin/bash

# Script to start the Vercel Load Balancer server

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please create .env file with required configuration"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check PocketBase configuration
if [ -z "$POCKETBASE_URL" ] || [ -z "$POCKETBASE_EMAIL" ] || [ -z "$POCKETBASE_PASSWORD" ]; then
    echo "⚠️  Warning: PocketBase configuration missing!"
    echo "   Please set POCKETBASE_URL, POCKETBASE_EMAIL, and POCKETBASE_PASSWORD in .env"
    exit 1
fi

echo "🚀 Starting Vercel Load Balancer Server..."
echo "   Port: ${PORT:-8000}"
echo "   Host: ${HOST:-0.0.0.0}"
echo ""

# Start server
python3 server.py
