#!/usr/bin/env python3
"""
CLI tool for managing Load Balancer API keys.
Usage:
    python cli.py create-key --name "My App" --rate-limit 60 --expires 30
    python cli.py list-keys
    python cli.py get-key <key-id>
    python cli.py delete-key <key-id>
    python cli.py update-key <key-id> --name "New Name" --rate-limit 100
    python cli.py key-stats <key-id>
"""

import argparse
import asyncio
import sys
from datetime import datetime, timezone
from tabulate import tabulate

from database import (
    init_database, create_key, list_keys, get_key_by_id,
    update_key, delete_key, get_key_stats
)


def format_datetime(dt: datetime) -> str:
    """Format datetime for display."""
    if dt is None:
        return "Never"
    return dt.strftime("%Y-%m-%d %H:%M:%S")


async def cmd_create_key(args):
    """Create a new API key."""
    await init_database()
    
    raw_key, api_key = await create_key(
        name=args.name,
        rate_limit=args.rate_limit,
        expires_in_days=args.expires
    )
    
    print("\n" + "=" * 60)
    print("✓ API Key Created Successfully!")
    print("=" * 60)
    print(f"\n  API Key: {raw_key}")
    print(f"\n  ⚠️  SAVE THIS KEY NOW - IT WILL NOT BE SHOWN AGAIN!")
    print("\n" + "-" * 60)
    print(f"  ID:         {api_key.id}")
    print(f"  Name:       {api_key.name}")
    print(f"  Rate Limit: {api_key.rate_limit} req/min" if api_key.rate_limit > 0 else "  Rate Limit: Unlimited")
    print(f"  Expires:    {format_datetime(api_key.expires_at)}")
    print(f"  Created:    {format_datetime(api_key.created_at)}")
    print("=" * 60 + "\n")


async def cmd_list_keys(args):
    """List all API keys."""
    await init_database()
    
    keys = await list_keys()
    
    if not keys:
        print("\nNo API keys found.\n")
        return
    
    table_data = []
    for key in keys:
        status = "✓ Active" if key.is_active else "✗ Inactive"
        
        # Check if expired
        if key.expires_at and key.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
            status = "⏰ Expired"
        
        rate = f"{key.rate_limit}/min" if key.rate_limit > 0 else "Unlimited"
        
        table_data.append([
            key.id[:8] + "...",
            key.name,
            status,
            rate,
            format_datetime(key.expires_at),
            format_datetime(key.created_at)
        ])
    
    headers = ["ID", "Name", "Status", "Rate Limit", "Expires", "Created"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid") + "\n")
    print(f"Total: {len(keys)} key(s)\n")


async def cmd_get_key(args):
    """Get details for a specific key."""
    await init_database()
    
    api_key = await get_key_by_id(args.key_id)
    
    if not api_key:
        print(f"\n✗ Key not found: {args.key_id}\n")
        sys.exit(1)
    
    status = "Active" if api_key.is_active else "Inactive"
    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        status = "Expired"
    
    print("\n" + "=" * 50)
    print(f"API Key Details: {api_key.name}")
    print("=" * 50)
    print(f"  ID:         {api_key.id}")
    print(f"  Name:       {api_key.name}")
    print(f"  Status:     {status}")
    print(f"  Rate Limit: {api_key.rate_limit} req/min" if api_key.rate_limit > 0 else "  Rate Limit: Unlimited")
    print(f"  Expires:    {format_datetime(api_key.expires_at)}")
    print(f"  Created:    {format_datetime(api_key.created_at)}")
    print("=" * 50 + "\n")


async def cmd_delete_key(args):
    """Delete an API key."""
    await init_database()
    
    # Confirm deletion
    if not args.yes:
        api_key = await get_key_by_id(args.key_id)
        if not api_key:
            print(f"\n✗ Key not found: {args.key_id}\n")
            sys.exit(1)
        
        confirm = input(f"\nAre you sure you want to delete key '{api_key.name}'? [y/N]: ")
        if confirm.lower() != 'y':
            print("Cancelled.\n")
            return
    
    success = await delete_key(args.key_id)
    
    if success:
        print(f"\n✓ Key deleted: {args.key_id}\n")
    else:
        print(f"\n✗ Key not found: {args.key_id}\n")
        sys.exit(1)


async def cmd_update_key(args):
    """Update an API key."""
    await init_database()
    
    # Check if key exists
    existing = await get_key_by_id(args.key_id)
    if not existing:
        print(f"\n✗ Key not found: {args.key_id}\n")
        sys.exit(1)
    
    # Build update params
    expires_at = None
    if args.expires is not None:
        if args.expires > 0:
            from datetime import timedelta
            expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=args.expires)
    
    is_active = None
    if args.activate:
        is_active = True
    elif args.deactivate:
        is_active = False
    
    updated = await update_key(
        key_id=args.key_id,
        name=args.name,
        rate_limit=args.rate_limit,
        is_active=is_active,
        expires_at=expires_at
    )
    
    print(f"\n✓ Key updated: {updated.name}")
    print(f"  Rate Limit: {updated.rate_limit} req/min" if updated.rate_limit > 0 else "  Rate Limit: Unlimited")
    print(f"  Active: {updated.is_active}")
    print(f"  Expires: {format_datetime(updated.expires_at)}\n")


async def cmd_key_stats(args):
    """Show usage statistics for a key."""
    await init_database()
    
    api_key = await get_key_by_id(args.key_id)
    if not api_key:
        print(f"\n✗ Key not found: {args.key_id}\n")
        sys.exit(1)
    
    stats = await get_key_stats(args.key_id)
    
    print("\n" + "=" * 50)
    print(f"Usage Statistics: {api_key.name}")
    print("=" * 50)
    print(f"  Total Requests: {stats['total_requests']}")
    print(f"  Total Tokens:   {stats['total_tokens']}")
    
    if stats['by_endpoint']:
        print("\n  By Endpoint:")
        for endpoint, count in stats['by_endpoint'].items():
            print(f"    {endpoint}: {count}")
    
    if stats['by_model']:
        print("\n  By Model:")
        for model, count in stats['by_model'].items():
            print(f"    {model}: {count}")
    
    if stats['recent_requests']:
        print("\n  Recent Requests:")
        for req in stats['recent_requests'][:5]:
            model_str = f" ({req['model']})" if req['model'] else ""
            tokens_str = f" - {req['tokens_used']} tokens" if req['tokens_used'] else ""
            print(f"    {req['timestamp']} - {req['endpoint']}{model_str}{tokens_str}")
    
    print("=" * 50 + "\n")


async def cmd_init(args):
    """Initialize the database."""
    await init_database()
    print("\n✓ Database initialized successfully.\n")


def main():
    parser = argparse.ArgumentParser(
        description="Load Balancer API Key Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # init command
    init_parser = subparsers.add_parser("init", help="Initialize the database")
    init_parser.set_defaults(func=cmd_init)
    
    # create-key command
    create_parser = subparsers.add_parser("create-key", help="Create a new API key")
    create_parser.add_argument("--name", "-n", required=True, help="Name for the API key")
    create_parser.add_argument("--rate-limit", "-r", type=int, default=0, 
                               help="Rate limit in requests per minute (0 = unlimited)")
    create_parser.add_argument("--expires", "-e", type=int, default=None,
                               help="Expiration in days (default: never)")
    create_parser.set_defaults(func=cmd_create_key)
    
    # list-keys command
    list_parser = subparsers.add_parser("list-keys", help="List all API keys")
    list_parser.set_defaults(func=cmd_list_keys)
    
    # get-key command
    get_parser = subparsers.add_parser("get-key", help="Get details for a specific key")
    get_parser.add_argument("key_id", help="The key ID")
    get_parser.set_defaults(func=cmd_get_key)
    
    # delete-key command
    delete_parser = subparsers.add_parser("delete-key", help="Delete an API key")
    delete_parser.add_argument("key_id", help="The key ID")
    delete_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    delete_parser.set_defaults(func=cmd_delete_key)
    
    # update-key command
    update_parser = subparsers.add_parser("update-key", help="Update an API key")
    update_parser.add_argument("key_id", help="The key ID")
    update_parser.add_argument("--name", "-n", help="New name")
    update_parser.add_argument("--rate-limit", "-r", type=int, help="New rate limit")
    update_parser.add_argument("--expires", "-e", type=int, help="New expiration in days")
    update_parser.add_argument("--activate", action="store_true", help="Activate the key")
    update_parser.add_argument("--deactivate", action="store_true", help="Deactivate the key")
    update_parser.set_defaults(func=cmd_update_key)
    
    # key-stats command
    stats_parser = subparsers.add_parser("key-stats", help="Show usage statistics for a key")
    stats_parser.add_argument("key_id", help="The key ID")
    stats_parser.set_defaults(func=cmd_key_stats)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Run the async command
    asyncio.run(args.func(args))


if __name__ == "__main__":
    main()

