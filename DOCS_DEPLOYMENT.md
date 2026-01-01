# Documentation Website Deployment Guide

## 🌐 Live Documentation

The documentation website is automatically deployed to GitHub Pages and is available at:
**[https://newnol.github.io/Vercel-API-Key/](https://newnol.github.io/Vercel-API-Key/)**

## 🚀 Automatic Deployment

The documentation is automatically deployed via GitHub Actions whenever changes are pushed to the `main` branch that affect the `docs/` directory.

### GitHub Pages Setup

1. Go to your repository settings on GitHub
2. Navigate to **Pages** section
3. Under **Build and deployment**, select:
   - Source: **GitHub Actions**
4. The workflow file is located at `.github/workflows/deploy-docs.yml`

## 🔧 Manual Deployment

If you need to deploy manually:

```bash
cd docs
npm run build
GIT_USER=newnol npm run deploy
```

This will build the site and push to the `gh-pages` branch.

## 💻 Local Development

To run the documentation site locally:

```bash
cd docs
npm install
npm start
```

The site will be available at `http://localhost:3000/Vercel-API-Key/`

## 📝 Updating Documentation

1. Edit markdown files in `docs/docs/` directory
2. Test locally with `npm start`
3. Commit and push to `main` branch
4. GitHub Actions will automatically deploy

## 🔍 Monitoring Deployment

Check deployment status:
- Go to **Actions** tab in GitHub repository
- Look for "Deploy Docusaurus to GitHub Pages" workflow
- Click on the latest run to see logs

## ❓ Troubleshooting

### Build Fails
- Check the Actions log for errors
- Ensure all markdown links are valid
- Verify `docusaurus.config.ts` is correct

### Site Not Updating
- Clear browser cache
- Wait a few minutes for CDN propagation
- Check if workflow ran successfully

### 404 on GitHub Pages
- Verify `baseUrl` in `docusaurus.config.ts` is `/Vercel-API-Key/`
- Ensure GitHub Pages is enabled in repository settings
- Check that `gh-pages` branch exists

## 📚 Resources

- [Docusaurus Deployment Guide](https://docusaurus.io/docs/deployment)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
