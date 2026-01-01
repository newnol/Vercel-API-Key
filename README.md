# Vercel AI Gateway Load Balancer

Một FastAPI server hoạt động như reverse proxy cho Vercel AI Gateway với tính năng load balancing dựa trên credit balance và hệ thống xác thực API key.

## 📚 Documentation

🌐 **[View Full Documentation Website](https://newnol.github.io/Vercel-API-Key/)** - Built with Docusaurus

Tài liệu đầy đủ bao gồm:
- **[Quick Start](https://newnol.github.io/Vercel-API-Key/quickstart)** - Hướng dẫn bắt đầu nhanh
- **[API Reference](https://newnol.github.io/Vercel-API-Key/api)** - Chi tiết API endpoints
- **[Deployment](https://newnol.github.io/Vercel-API-Key/deployment)** - Hướng dẫn deploy với Docker
- **[Project Structure](https://newnol.github.io/Vercel-API-Key/project-structure)** - Cấu trúc dự án
- **[Contributing](https://newnol.github.io/Vercel-API-Key/contributing)** - Hướng dẫn đóng góp

## Tính năng

- ✅ **Load Balancing thông minh**: Tự động chọn Vercel API key dựa trên số credit còn lại (weighted random)
- ✅ **Xác thực API Key**: Client phải có API key hợp lệ mới có thể sử dụng
- ✅ **Rate Limiting**: Giới hạn số requests/phút cho mỗi API key
- ✅ **Usage Tracking**: Theo dõi số requests, tokens, models đã sử dụng
- ✅ **Expiry Date**: Hỗ trợ API key có thời hạn sử dụng
- ✅ **Admin API**: Quản lý keys qua REST API
- ✅ **CLI Tool**: Quản lý keys qua command line
- ✅ **100% OpenAI Compatible**: Hỗ trợ tất cả endpoints và streaming
- 🔒 **Security**: Pre-commit hooks với Gitleaks để ngăn chặn secrets bị commit

## Adding Translations

To add or update translations for a specific language:

1. **Generate translation files** (for UI elements):
   ```bash
   npm run write-translations -- --locale en
   ```

2. **Translate Documentation**:
   - Create/Update files in `i18n/en/docusaurus-plugin-content-docs/current/`
   - Ensure filenames match the source files in `docs/`
   - Keep the same frontmatter (id, sidebar_position)

3. **Folder Structure**:
   ```
   docs/
   ├── docs/                   # Vietnamese (Source)
   │   ├── intro.md
   │   └── ...
   └── i18n/
       └── en/                 # English (Translation)
           └── docusaurus-plugin-content-docs/
               └── current/
                   ├── intro.md
                   └── ...
   ```

**Supported Languages:**
- `vi` (Vietnamese) - Default
- `en` (English)
