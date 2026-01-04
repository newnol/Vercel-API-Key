# syntax=docker/dockerfile:1
# Multi-stage build for optimized Docker image
FROM python:3.13-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies with cache
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# Final stage
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application files
COPY *.py ./
COPY config/ ./config/

# Create directory for database and output
RUN mkdir -p /app/data /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV HOST=0.0.0.0
ENV DATABASE_PATH=/app/data/lb_database.db

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the server
CMD ["python", "server.py"]
