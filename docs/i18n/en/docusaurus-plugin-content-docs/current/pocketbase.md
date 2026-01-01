---
sidebar_position: 8
title: PocketBase Integration
---

# PocketBase Integration

Documentation for PocketBase integration.

## Configuration

### PocketBase Server
- **Base URL**: `https://base.selfhost.io.vn`
- **Collection**: `Vercel_api_key`

### Authentication

Script uses superuser authentication to access PocketBase:

- **Endpoint**: `/api/collections/_superusers/auth-with-password`
- **Method**: POST
- **Body**:
  ```json
  {
    "identity": "your-email@example.com",
    "password": "your-password"
  }
  ```

## Usage

### 1. Run test script

```bash
# From project root
cd pocketbase
python test-pocketbase.py

# Or from root
python pocketbase/test-pocketbase.py
```

### 2. Functions

The `test-pocketbase.py` script provides:

#### `admin_login()`
Login with superuser account and get authentication token.

#### `test_list_records(page, per_page, expand, use_bearer)`
Get list of records from collection.
