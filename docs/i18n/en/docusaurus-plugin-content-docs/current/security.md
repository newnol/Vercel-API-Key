---
sidebar_position: 4
title: Security Cleanup
---

# 🔒 Security Guide - Remove Secrets From Git History

## ⚠️ WARNING: Backup before proceeding!

## Method 1: Using BFG Repo-Cleaner (Recommended)

### Step 1: Install BFG
```bash
brew install bfg
```

### Step 2: Create file with secrets to remove
Create `secrets.txt` file with content:
```
vck_1ISL6iPcztZ8owzOBPvGHPzBF0cJNa00bAP17LThxXro43V5c13L7aEf
vck_5GvPArwaNvzGKUvWMH9qbZ5HJvTvQnX3hNNyPx1zpPWnZjlGQz0Maowv
sk-lb-nzluPs0KFHPSk9PmBYl4heg29ZNJO_uT
your-admin-secret
your-password
```

### Step 3: Clone mirror of repo
```bash
cd ..
git clone --mirror https://github.com/newnol/Vercel-API-Key.git Vercel-API-Key-mirror
```

### Step 4: Run BFG to remove secrets
```bash
bfg --replace-text secrets.txt Vercel-API-Key-mirror
```

### Step 5: Cleanup and force push
```bash
cd Vercel-API-Key-mirror
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

### Step 6: Update local repo
```bash
cd ../Vercel-API-Key
git pull --rebase
```

---

## Method 2: Using git-filter-repo (More Precise)

### Step 1: Install git-filter-repo
```bash
brew install git-filter-repo
```

### Step 2: Remove sensitive files from entire history
```bash
# Remove .env file from entire history
git filter-repo --path .env --invert-paths

# Remove tests/.env
git filter-repo --path tests/.env --invert-paths

# Remove config/key-list.json (keep current version)
git filter-repo --path config/key-list.json --invert-paths
```

### Step 3: Force push
```bash
git remote add origin https://github.com/newnol/Vercel-API-Key.git
git push --force --all
git push --force --tags
```

---

## Method 3: Remove Specific Files from History

If you only want to completely remove certain files:

```bash
# Remove .env from entire history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Remove tests/.env
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch tests/.env" \
  --prune-empty --tag-name-filter cat -- --all

# Cleanup
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push --force --all
```

---

## ✅ After Cleaning History

1. **Revoke all API keys**:
   - Access Vercel Dashboard
   - Delete/reset all leaked keys
   - Create new keys

2. **Revoke PocketBase credentials**:
   - Change password for exposed accounts
   - Update ADMIN_SECRET

3. **Update .env with new keys**:
   ```bash
   cp .env.example .env
   # Fill in new information in .env
   ```

4. **Notify team members**:
   ```bash
   # All members need to run:
   git fetch origin
   git reset --hard origin/main
   ```

5. **Verify again**:
   ```bash
   gitleaks detect --verbose
   ```

---

## 🛡️ Future Protection

Pre-commit hooks have been installed and will automatically scan for secrets before each commit. To test:

```bash
# Try committing a file with secret
echo "api_key=sk-test123" > test.txt
git add test.txt
git commit -m "test"
# → Hook will BLOCK this commit!

# Cleanup
rm test.txt
```

---

## 📞 If You Need Help

- Gitleaks docs: https://github.com/gitleaks/gitleaks
- BFG docs: https://rtyley.github.io/bfg-repo-cleaner/
- git-filter-repo: https://github.com/newren/git-filter-repo
