# 🚀 Deploying AgroMind AI to Render

## Prerequisites

1. **GitHub Account**: Push your code to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Step-by-Step Deployment Guide

### 1. Prepare Your Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AgroMind AI"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/agromind-ai.git
git branch -M main
git push -u origin main
```

### 2. Deploy Backend on Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → Select **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Name**: `agromind-ai-backend`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT`

5. **Add Environment Variables**:
   - Click **"Environment"** tab
   - Add the following variables:
     ```
     GEMINI_API_KEY=your_actual_gemini_api_key_here
     FLASK_ENV=production
     FLASK_DEBUG=False
     PORT=10000
     CORS_ORIGINS=*
     ```

6. **Click "Create Web Service"**

### 3. Deploy Frontend (Static Site)

**Option A: Deploy on Render**

1. **Click "New +"** → Select **"Static Site"**
2. **Connect same repository**
3. **Configure**:
   - **Name**: `agromind-ai-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: Leave empty
   - **Publish Directory**: `.`

4. **Update API URL**:
   - After backend deploys, copy its URL (e.g., `https://agromind-ai-backend.onrender.com`)
   - Update `frontend/app.js` line 4:
     ```javascript
     const API_BASE_URL = 'https://agromind-ai-backend.onrender.com/api';
     ```
   - Commit and push changes

**Option B: Deploy on Netlify/Vercel (Recommended for frontend)**

1. Go to [Netlify](https://netlify.com) or [Vercel](https://vercel.com)
2. Import your GitHub repository
3. Set **Publish directory**: `frontend`
4. Deploy!

### 4. Verify Deployment

1. **Test Backend**:
   ```bash
   curl https://agromind-ai-backend.onrender.com/api/health
   ```

2. **Test Frontend**:
   - Open your frontend URL
   - Try crop predictions
   - Test AI Agronomist

## Important Notes

### Free Tier Limitations

- **Render Free Tier**: 
  - Service spins down after 15 minutes of inactivity
  - First request after spin-down takes ~30 seconds
  - 750 hours/month free

### Model Files

- Model files (`backend/models/`) are generated during build
- They persist across deploys but not across service restarts on free tier
- Consider upgrading to paid tier for production use

### Environment Variables

**Never commit** your `.env` file to GitHub! It's already in `.gitignore`.

Always set environment variables in Render dashboard.

## Troubleshooting

### Build Fails

**Issue**: Model training times out
**Solution**: 
- Upgrade to paid tier for more build time
- Or pre-train model and commit to repo (not recommended for large models)

### CORS Errors

**Issue**: Frontend can't access backend
**Solution**: 
- Ensure `CORS_ORIGINS=*` in backend environment variables
- Or set specific frontend URL: `CORS_ORIGINS=https://your-frontend.netlify.app`

### API Key Not Working

**Issue**: AI Agronomist returns errors
**Solution**:
- Verify `GEMINI_API_KEY` is set correctly in Render dashboard
- Check API key is valid at Google AI Studio
- Ensure no extra spaces in the key

## Updating Your Deployment

```bash
# Make changes to your code
git add .
git commit -m "Your update message"
git push

# Render will automatically rebuild and deploy!
```

## Production Checklist

- [ ] Set `FLASK_DEBUG=False` in production
- [ ] Use strong API keys
- [ ] Set specific CORS origins (not `*`)
- [ ] Monitor usage and costs
- [ ] Set up custom domain (optional)
- [ ] Enable HTTPS (automatic on Render)
- [ ] Set up monitoring/logging

## Cost Optimization

1. **Free Tier**: Good for testing and demos
2. **Starter Plan** ($7/month): 
   - No spin-down
   - Better for production
   - Persistent storage

## Support

- **Render Docs**: https://render.com/docs
- **Flask Deployment**: https://flask.palletsprojects.com/en/3.0.x/deploying/

---

🎉 **Your AgroMind AI is now live!** Share the URL with farmers and agronomists!
