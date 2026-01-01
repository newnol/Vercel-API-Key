# 🔒 Hướng Dẫn Bảo Mật - Xóa Secrets Khỏi Git History

## ⚠️ CẨN TRỌNG: Làm backup trước khi thực hiện!

## Phương Pháp 1: Sử dụng BFG Repo-Cleaner (Khuyến nghị)

### Bước 1: Cài đặt BFG
```bash
brew install bfg
```

### Bước 2: Tạo file chứa các secrets cần xóa
Tạo file `secrets.txt` với nội dung:
```
vck_1ISL6iPcztZ8owzOBPvGHPzBF0cJNa00bAP17LThxXro43V5c13L7aEf
vck_5GvPArwaNvzGKUvWMH9qbZ5HJvTvQnX3hNNyPx1zpPWnZjlGQz0Maowv
vck_6kxrTHOajjaxPvokdqHo4YCYq6K2dksHogzhjVK9nHYZY2Lx8j31f5v3
vck_0U000kJYhNAa6PMCfaeBWOESSPY5UmgEtn4vpXsMPdEMr2dvDl2MRgbo
vck_7ffL04ULR6Niw8ePoSLeAFVTbPl4u5R2FAjWNhkYxmQamY1De50J4I5o
vck_0pVDPlLLaqtXweLKURhWGEkpBn8lAIpNpILSNkhlv4c8cPvg1J1CBRS7
vck_6S1q789MAZblLQMPNncru5AAM5pvA6z5jcJGouhF49S8ivLLDV0elAH4
vck_1miapeAdJZEk0eJGZBMRIvBIOhQI7rlfHsEzSYyN9q8CKERhJp0yLu6y
vck_3dWx7LptIXKHSsTIc6TerrdccZBqmHsWDBiUNYo4fXE19XBOJl46flsd
vck_0GyhZ4bhPplVvBebkyJUwUOLDPRcnGIXRy7OsuFkmuS68iaMQz3NjwV2
sk-lb-nzluPs0KFHPSk9PmBYl4heg29ZNJO_uT
sk-lb-LuVvR3CE-iKzPGHafeAP7xszMzDRaPCM
sk-lb-JvyUvt9xdADNUOrq_U_PaGqpGh8RrZkL
newnol
tantai13102005@gmail.com
ngotantai123
```

### Bước 3: Clone một mirror của repo
```bash
cd ..
git clone --mirror https://github.com/newnol/Vercel-API-Key.git Vercel-API-Key-mirror
```

### Bước 4: Chạy BFG để xóa secrets
```bash
bfg --replace-text secrets.txt Vercel-API-Key-mirror
```

### Bước 5: Dọn dẹp và force push
```bash
cd Vercel-API-Key-mirror
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

### Bước 6: Cập nhật local repo
```bash
cd ../Vercel-API-Key
git pull --rebase
```

---

## Phương Pháp 2: Sử dụng git-filter-repo (Chính xác hơn)

### Bước 1: Cài đặt git-filter-repo
```bash
brew install git-filter-repo
```

### Bước 2: Xóa các file nhạy cảm khỏi toàn bộ lịch sử
```bash
# Xóa file .env khỏi toàn bộ lịch sử
git filter-repo --path .env --invert-paths

# Xóa tests/.env
git filter-repo --path tests/.env --invert-paths

# Xóa config/key-list.json (giữ lại version hiện tại)
git filter-repo --path config/key-list.json --invert-paths
```

### Bước 3: Force push
```bash
git remote add origin https://github.com/newnol/Vercel-API-Key.git
git push --force --all
git push --force --tags
```

---

## Phương Pháp 3: Xóa file cụ thể khỏi lịch sử

Nếu bạn chỉ muốn xóa hoàn toàn một số file:

```bash
# Xóa .env khỏi toàn bộ lịch sử
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Xóa tests/.env
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch tests/.env" \
  --prune-empty --tag-name-filter cat -- --all

# Dọn dẹp
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push --force --all
```

---

## ✅ Sau khi làm sạch lịch sử

1. **Thu hồi tất cả API keys**:
   - Truy cập Vercel Dashboard
   - Xóa/reset tất cả keys đã bị lộ
   - Tạo keys mới

2. **Thu hồi PocketBase credentials**:
   - Đổi password của tài khoản `tantai13102005@gmail.com`
   - Cập nhật ADMIN_SECRET

3. **Cập nhật .env với keys mới**:
   ```bash
   cp .env.example .env
   # Điền thông tin mới vào .env
   ```

4. **Thông báo cho team members**:
   ```bash
   # Tất cả thành viên cần chạy:
   git fetch origin
   git reset --hard origin/main
   ```

5. **Kiểm tra lại**:
   ```bash
   gitleaks detect --verbose
   ```

---

## 🛡️ Bảo vệ trong tương lai

Pre-commit hook đã được cài đặt sẽ tự động quét secrets trước mỗi commit. Để test:

```bash
# Thử commit một file có secret
echo "api_key=sk-test123" > test.txt
git add test.txt
git commit -m "test"
# Hook sẽ chặn commit này!
```

---

## 📞 Nếu cần hỗ trợ

- Gitleaks docs: https://github.com/gitleaks/gitleaks
- BFG docs: https://rtyley.github.io/bfg-repo-cleaner/
- git-filter-repo: https://github.com/newren/git-filter-repo
