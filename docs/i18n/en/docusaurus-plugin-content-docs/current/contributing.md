---
sidebar_position: 5
title: Contributing
---

# Contributing Guidelines

Thank you for your interest in contributing to Vercel AI Gateway Load Balancer!

## 🚀 Getting Started

### 1. Fork and Clone Repository

```bash
git clone https://github.com/newnol/Vercel-API-Key.git
cd Vercel-API-Key
```

### 2. Setup Development Environment

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks (REQUIRED)
pip install pre-commit
pre-commit install
```

### 3. Configure Environment

```bash
# Copy and configure .env
cp .env.example .env

# Generate strong ADMIN_SECRET
echo "ADMIN_SECRET=$(openssl rand -hex 32)" >> .env
```

### 4. Initialize Database for Testing

```bash
python cli.py init
```

## 🔒 Security Requirements

### Pre-commit Hooks

Project uses pre-commit hooks with **Gitleaks** to prevent secrets from being committed:

- ✅ Automatically runs before each commit
- ✅ Scans for API keys, passwords, tokens
- ✅ Blocks commit if secrets detected

**Note:** If hook blocks your commit, check and remove secrets before committing again.

### Do Not Commit Secrets

**NEVER** commit these files:
- `.env` - Environment variables
- `config/key-list.json` - Vercel API keys
- `tests/.env` - Test API keys
- `lb_database.db` - Database may contain sensitive data
- `gitleaks-report.json` - Gitleaks scan results

These files are already in `.gitignore`.

### Testing Pre-commit Hooks

```bash
# Test hook works correctly
echo "api_key=sk-test123" > test.txt
git add test.txt
git commit -m "test"
# → Hook will BLOCK this commit

# Cleanup
rm test.txt
```

## 📝 Development Workflow

### 1. Create New Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

- Write clear, easy-to-understand code
- Follow Python best practices (PEP 8)
- Add docstrings for functions/classes
- Update tests if needed

### 3. Test Changes

```bash
# Run tests
python -m pytest tests/

# Test specific file
python tests/test-api-key.py

# Test server locally
python server.py
```

### 4. Commit Changes

```bash
# Add files
git add .

# Commit (pre-commit hooks will run automatically)
git commit -m "feat: add new feature"

# If hooks fail, fix issues and commit again
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create Pull Request on GitHub.

## 📋 Commit Message Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]
[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat: add image generation endpoint"
git commit -m "fix: resolve rate limiting issue"
git commit -m "docs: update API documentation"
git commit -m "chore: update dependencies"
```

## 🧪 Testing

### Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific test
python tests/test-api-key.py

# With coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Writing Tests

When adding new features, add corresponding tests:

```python
# tests/test_your_feature.py
def test_your_feature():
    # Arrange
    # Act
    # Assert
    pass
```

## 🐛 Reporting Issues

When reporting issues, include:

1. **Problem description**: Clear and detailed
2. **Steps to reproduce**: Steps to reproduce the error
3. **Expected behavior**: Expected result
4. **Actual behavior**: Actual result
5. **Environment**: Python version, OS, etc.
6. **Logs**: Error messages or relevant logs

## 🎨 Code Style

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Max line length: 100 characters
- Use meaningful variable names

### Pre-commit Checks

Pre-commit will automatically check:
- Trailing whitespace
- End of file fixing
- YAML syntax
- Large files
- Merge conflicts
- Private keys
- **Gitleaks** (secrets detection)

## 🔐 Security Guidelines

### API Keys & Secrets

1. **Never hardcode** API keys, passwords, or tokens
2. **Always use** environment variables
3. **Use `.env.example`** for templates
4. **Test with dummy data**, don't use production keys

## 📚 Documentation

When adding new features, update docs:

- `README.md` - Main documentation
- `API.md` - API endpoints documentation
- `QUICKSTART.md` - Quick start guide
- Docstrings in code
- Comments for complex logic

## � Testing

The `tests/` directory contains test files and scripts.

### Files

- `test-api-key.py` - Test API key with OpenAI client
- `test-pocketbase-connection.py` - Test PocketBase connection (if used)
- `test-pocketbase.py` - Detailed PocketBase test script

### Usage

```bash
# Test API key (server must be running)
python tests/test-api-key.py

# Test PocketBase connection
python tests/test-pocketbase-connection.py
```

## 🛠 Utility Scripts

The `scripts/` directory contains utility and helper scripts.

### Files

- `start-server.sh` - Script to start server
- `generate-image.py` - Script to generate images
- `track-credit.py` - Script to track credit usage

### Usage

```bash
# Start server
./scripts/start-server.sh

# Generate image
python scripts/generate-image.py
```

## �🤝 Pull Request Process

1. **Fork** repository
2. **Create branch** from `main`
3. **Make changes** and commit
4. **Push** to your fork
5. **Create PR** with clear description
6. **Address review comments** if any
7. **Wait for approval** and merge

## ❓ Questions?

If you have questions:
1. Check [Introduction](intro) and [API Reference](api)
2. Search existing issues
3. Create new issue with "question" label

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
