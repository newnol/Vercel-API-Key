"""
Database module for Load Balancer API Key management.
Uses SQLite with aiosqlite for async operations.
"""

import aiosqlite
import hashlib
import secrets
import uuid
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from dataclasses import dataclass

# Support environment variable for database path (useful for Docker)
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/lb_database.db")

@dataclass
class APIKey:
    id: str
    key_hash: str
    name: str
    created_at: datetime
    expires_at: Optional[datetime]
    rate_limit: int  # requests per minute, 0 = unlimited
    is_active: bool

@dataclass
class UsageLog:
    id: int
    key_id: str
    timestamp: datetime
    endpoint: str
    tokens_used: Optional[int]
    model: Optional[str]


def hash_key(key: str) -> str:
    """Hash an API key using SHA256."""
    return hashlib.sha256(key.encode()).hexdigest()


def generate_api_key() -> str:
    """Generate a new API key in format sk-lb-{32_random_chars}."""
    random_part = secrets.token_urlsafe(24)  # ~32 chars
    return f"sk-lb-{random_part}"


async def init_database():
    """Initialize the database with required tables."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Create api_keys table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id TEXT PRIMARY KEY,
                key_hash TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT,
                rate_limit INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1
            )
        """)

        # Create usage_logs table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                tokens_used INTEGER,
                model TEXT,
                FOREIGN KEY (key_id) REFERENCES api_keys(id)
            )
        """)

        # Create indexes for better performance
        await db.execute("CREATE INDEX IF NOT EXISTS idx_usage_key_id ON usage_logs(key_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_usage_timestamp ON usage_logs(timestamp)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_key_hash ON api_keys(key_hash)")

        await db.commit()


async def create_key(
    name: str,
    rate_limit: int = 0,
    expires_in_days: Optional[int] = None
) -> tuple[str, APIKey]:
    """
    Create a new API key.
    Returns tuple of (raw_key, APIKey object).
    The raw key is only returned once and should be given to the user.
    """
    key_id = str(uuid.uuid4())
    raw_key = generate_api_key()
    key_hash = hash_key(raw_key)
    created_at = datetime.now(timezone.utc).replace(tzinfo=None)
    expires_at = None

    if expires_in_days:
        expires_at = created_at + timedelta(days=expires_in_days)

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO api_keys (id, key_hash, name, created_at, expires_at, rate_limit, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                key_id,
                key_hash,
                name,
                created_at.isoformat(),
                expires_at.isoformat() if expires_at else None,
                rate_limit,
                1
            )
        )
        await db.commit()

    api_key = APIKey(
        id=key_id,
        key_hash=key_hash,
        name=name,
        created_at=created_at,
        expires_at=expires_at,
        rate_limit=rate_limit,
        is_active=True
    )

    return raw_key, api_key


async def validate_key(raw_key: str) -> Optional[APIKey]:
    """
    Validate an API key and return the APIKey object if valid.
    Returns None if key is invalid, expired, or inactive.
    """
    key_hash = hash_key(raw_key)

    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM api_keys WHERE key_hash = ?",
            (key_hash,)
        ) as cursor:
            row = await cursor.fetchone()

            if not row:
                return None

            # Check if active
            if not row["is_active"]:
                return None

            # Check expiry
            expires_at = None
            if row["expires_at"]:
                expires_at = datetime.fromisoformat(row["expires_at"])
                if expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
                    return None

            return APIKey(
                id=row["id"],
                key_hash=row["key_hash"],
                name=row["name"],
                created_at=datetime.fromisoformat(row["created_at"]),
                expires_at=expires_at,
                rate_limit=row["rate_limit"],
                is_active=bool(row["is_active"])
            )


async def get_key_by_id(key_id: str) -> Optional[APIKey]:
    """Get an API key by its ID."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM api_keys WHERE id = ?",
            (key_id,)
        ) as cursor:
            row = await cursor.fetchone()

            if not row:
                return None

            expires_at = None
            if row["expires_at"]:
                expires_at = datetime.fromisoformat(row["expires_at"])

            return APIKey(
                id=row["id"],
                key_hash=row["key_hash"],
                name=row["name"],
                created_at=datetime.fromisoformat(row["created_at"]),
                expires_at=expires_at,
                rate_limit=row["rate_limit"],
                is_active=bool(row["is_active"])
            )


async def list_keys() -> list[APIKey]:
    """List all API keys."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM api_keys ORDER BY created_at DESC") as cursor:
            rows = await cursor.fetchall()

            keys = []
            for row in rows:
                expires_at = None
                if row["expires_at"]:
                    expires_at = datetime.fromisoformat(row["expires_at"])

                keys.append(APIKey(
                    id=row["id"],
                    key_hash=row["key_hash"],
                    name=row["name"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    expires_at=expires_at,
                    rate_limit=row["rate_limit"],
                    is_active=bool(row["is_active"])
                ))

            return keys


async def update_key(
    key_id: str,
    name: Optional[str] = None,
    rate_limit: Optional[int] = None,
    is_active: Optional[bool] = None,
    expires_at: Optional[datetime] = None
) -> Optional[APIKey]:
    """Update an API key's properties."""
    # Build update query dynamically
    updates = []
    params = []

    if name is not None:
        updates.append("name = ?")
        params.append(name)

    if rate_limit is not None:
        updates.append("rate_limit = ?")
        params.append(rate_limit)

    if is_active is not None:
        updates.append("is_active = ?")
        params.append(1 if is_active else 0)

    if expires_at is not None:
        updates.append("expires_at = ?")
        params.append(expires_at.isoformat())

    if not updates:
        return await get_key_by_id(key_id)

    params.append(key_id)

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            f"UPDATE api_keys SET {', '.join(updates)} WHERE id = ?",
            params
        )
        await db.commit()

    return await get_key_by_id(key_id)


async def delete_key(key_id: str) -> bool:
    """Delete an API key and its usage logs."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Delete usage logs first
        await db.execute("DELETE FROM usage_logs WHERE key_id = ?", (key_id,))

        # Delete the key
        cursor = await db.execute("DELETE FROM api_keys WHERE id = ?", (key_id,))
        await db.commit()

        return cursor.rowcount > 0


async def log_usage(
    key_id: str,
    endpoint: str,
    tokens_used: Optional[int] = None,
    model: Optional[str] = None
):
    """Log an API request."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO usage_logs (key_id, timestamp, endpoint, tokens_used, model)
            VALUES (?, ?, ?, ?, ?)
            """,
            (key_id, datetime.now(timezone.utc).replace(tzinfo=None).isoformat(), endpoint, tokens_used, model)
        )
        await db.commit()


async def get_request_count_in_window(key_id: str, window_seconds: int = 60) -> int:
    """Get the number of requests made by a key in the given time window."""
    window_start = (datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(seconds=window_seconds)).isoformat()

    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            """
            SELECT COUNT(*) FROM usage_logs
            WHERE key_id = ? AND timestamp > ?
            """,
            (key_id, window_start)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def get_key_stats(key_id: str) -> dict:
    """Get usage statistics for a key."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row

        # Total requests
        async with db.execute(
            "SELECT COUNT(*) as count FROM usage_logs WHERE key_id = ?",
            (key_id,)
        ) as cursor:
            row = await cursor.fetchone()
            total_requests = row["count"]

        # Total tokens
        async with db.execute(
            "SELECT SUM(tokens_used) as total FROM usage_logs WHERE key_id = ? AND tokens_used IS NOT NULL",
            (key_id,)
        ) as cursor:
            row = await cursor.fetchone()
            total_tokens = row["total"] or 0

        # Requests by endpoint
        async with db.execute(
            """
            SELECT endpoint, COUNT(*) as count
            FROM usage_logs WHERE key_id = ?
            GROUP BY endpoint
            """,
            (key_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            by_endpoint = {row["endpoint"]: row["count"] for row in rows}

        # Requests by model
        async with db.execute(
            """
            SELECT model, COUNT(*) as count
            FROM usage_logs WHERE key_id = ? AND model IS NOT NULL
            GROUP BY model
            """,
            (key_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            by_model = {row["model"]: row["count"] for row in rows}

        # Recent requests (last 10)
        async with db.execute(
            """
            SELECT * FROM usage_logs WHERE key_id = ?
            ORDER BY timestamp DESC LIMIT 10
            """,
            (key_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            recent = [
                {
                    "timestamp": row["timestamp"],
                    "endpoint": row["endpoint"],
                    "tokens_used": row["tokens_used"],
                    "model": row["model"]
                }
                for row in rows
            ]

        return {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "by_endpoint": by_endpoint,
            "by_model": by_model,
            "recent_requests": recent
        }


# Sync wrapper for CLI usage
def init_database_sync():
    """Synchronous wrapper for init_database."""
    import asyncio
    asyncio.run(init_database())
