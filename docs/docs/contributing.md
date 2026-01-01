---
sidebar_position: 5
title: Contributing
---

# Contributing Guidelines

Cảm ơn bạn quan tâm đến việc đóng góp cho Vercel AI Gateway Load Balancer!

## 🚀 Getting Started

### 1. Fork và Clone Repository

```bash
git clone https://github.com/newnol/Vercel-API-Key.git
cd Vercel-API-Key
```

### 2. Setup Development Environment

```bash
# Tạo và kích hoạt virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Cài đặt pre-commit hooks (BẮT BUỘC)
pip install pre-commit
pre-commit install
```

### 3. Cấu hình môi trường

```bash
# Copy và cấu hình .env
cp .env.example .env

# Generate ADMIN_SECRET mạnh
echo "ADMIN_SECRET=$(openssl rand -hex 32)" >> .env
```

### 4. Khởi tạo database để test

```bash
python cli.py init
```

## 🔒 Security Requirements

### Pre-commit Hooks

Project sử dụng pre-commit hooks với **Gitleaks** để ngăn chặn secrets bị commit:

- ✅ Tự động chạy trước mỗi commit
- ✅ Quét API keys, passwords, tokens
- ✅ Chặn commit nếu phát hiện secrets

**Lưu ý:** Nếu hook chặn commit của bạn, kiểm tra và xóa secrets trước khi commit lại.

### Không Commit Secrets

**KHÔNG BAO GIỜ** commit các file sau:
- `.env` - Environment variables
- `config/key-list.json` - Vercel API keys
- `tests/.env` - Test API keys
- `lb_database.db` - Database có thể chứa sensitive data
- `gitleaks-report.json` - Gitleaks scan results

Các file này đã được thêm vào `.gitignore`.

### Testing Pre-commit Hooks

```bash
# Test hook hoạt động đúng
echo "api_key=sk-test123" > test.txt
git add test.txt
git commit -m "test"
# → Hook sẽ CHẶN commit này

# Dọn dẹp
rm test.txt
```

## 📝 Development Workflow

### 1. Tạo Branch Mới

```bash
git checkout -b feature/your-feature-name
# hoặc
git checkout -b fix/bug-description
```

### 2. Make Changes

- Viết code rõ ràng, dễ hiểu
- Follow Python best practices (PEP 8)
- Thêm docstrings cho functions/classes
- Update tests nếu cần

### 3. Test Changes

```bash
# Chạy tests
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

# Commit (pre-commit hooks sẽ chạy tự động)
git commit -m "feat: add new feature"

# Nếu hooks fail, fix issues và commit lại
```

### 5. Push và Create PR

```bash
git push origin feature/your-feature-name
```

Sau đó tạo Pull Request trên GitHub.

## 📋 Commit Message Convention

Sử dụng [Conventional Commits](https://www.conventionalcommits.org/):

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

Khi thêm features mới, thêm tests tương ứng:

```python
# tests/test_your_feature.py
def test_your_feature():
    # Arrange
    # Act
    # Assert
    pass
```

## 🐛 Reporting Issues

Khi báo cáo issues, bao gồm:

1. **Mô tả vấn đề**: Rõ ràng và chi tiết
2. **Steps to reproduce**: Các bước tái hiện lỗi
3. **Expected behavior**: Kết quả mong đợi
4. **Actual behavior**: Kết quả thực tế
5. **Environment**: Python version, OS, etc.
6. **Logs**: Error messages hoặc relevant logs

## 🎨 Code Style

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Max line length: 100 characters
- Use meaningful variable names

### Pre-commit Checks

Pre-commit sẽ tự động check:
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
4. **Test với dummy data**, không dùng production keys

### Code Review Security

Khi review PRs, check:
- [ ] Không có hardcoded secrets
- [ ] Sensitive data không được log
- [ ] Input validation đầy đủ
- [ ] Error messages không leak information
- [ ] Dependencies được update

## 📚 Documentation

Khi thêm features mới, update docs:

- `README.md` - Main documentation
- `API.md` - API endpoints documentation
- `QUICKSTART.md` - Quick start guide
- Docstrings trong code
- Comments cho logic phức tạp

## � Testing

Thư mục `tests/` chứa các file test và script kiểm tra.

### Files

- `test-api-key.py` - Test API key với OpenAI client
- `test-pocketbase-connection.py` - Test kết nối PocketBase (nếu sử dụng)
- `test-pocketbase.py` - Script test PocketBase chi tiết

### Cách sử dụng

```bash
# Test API key (cần server đang chạy)
python tests/test-api-key.py

# Test PocketBase connection
python tests/test-pocketbase-connection.py
```

## 🛠 Utility Scripts

Thư mục `scripts/` chứa các utility scripts và helper scripts.

### Files

- `start-server.sh` - Script để khởi động server
- `generate-image.py` - Script để generate images
- `track-credit.py` - Script để track credit usage

### Cách sử dụng

```bash
# Khởi động server
./scripts/start-server.sh

# Generate image
python scripts/generate-image.py
```

## �🤝 Pull Request Process

1. **Fork** repository
2. **Create branch** từ `main`
3. **Make changes** và commit
4. **Push** to your fork
5. **Create PR** với description rõ ràng
6. **Address review comments** nếu có
7. **Wait for approval** và merge

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested the changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests
- [ ] All tests pass
- [ ] No secrets committed
```

## ❓ Questions?

Nếu có câu hỏi, hãy:
1. Check [Introduction](intro) và [API Reference](api)
2. Search existing issues
3. Tạo issue mới với label "question"

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
