# Quick Start - Render Deployment

## 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

## 2. Deploy on Render

### Backend:
1. Go to https://dashboard.render.com
2. New+ → Web Service
3. Connect your repo
4. **Build Command**: `chmod +x build.sh && ./build.sh`
5. **Start Command**: `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT`
6. Add Environment Variable: `GEMINI_API_KEY=your_key`
7. Deploy!

### Frontend:
1. Update `frontend/app.js` line 4 with your backend URL
2. Deploy as Static Site on Render/Netlify/Vercel

## 3. Done! 🎉

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
