# Quick Deployment Guide

Since the browser automation encountered technical issues, follow these manual steps to deploy:

## Step 1: Create GitHub Repository (2 minutes)

1. Go to https://github.com/new
2. **Repository name:** `RIZZA` or `ai-reply-strategist`
3. **Description:** "AI-powered conversational assistant for message replies"
4. **Visibility:** Public (recommended for free tier benefits)
5. **DO NOT** check "Initialize with README" or add .gitignore (we already have these)
6. Click **"Create repository"**

## Step 2: Push Your Code

After creating the repository, GitHub will show you commands. Use these in your terminal:

```bash
# Add the remote (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/RIZZA.git

# Push the code
git push -u origin main
```

## Step 3: Deploy Backend to Railway (5 minutes)

1. Go to https://railway.app/
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Authorize Railway and select your `RIZZA` repository
6. Click on the created service
7. Go to **Settings** → Set **Root Directory** to `backend`
8. Go to **Variables** → Add:
   - `OPENAI_API_KEY` = your actual OpenAI API key
9. Go to **Settings** → **Networking** → Click **"Generate Domain"**
10. **Copy the generated URL** (e.g., `https://rizza-production-xxx.railway.app`)

## Step 4: Update Frontend Environment

Update the file `frontend/.env.production`:
```env
NEXT_PUBLIC_API_URL=https://YOUR_RAILWAY_URL.railway.app/api/v1
```

Commit and push:
```bash
git add frontend/.env.production
git commit -m "Update production API URL"
git push origin main
```

## Step 5: Deploy Frontend to Vercel (5 minutes)

1. Go to https://vercel.com/
2. Sign in with GitHub
3. Click **"Add New"** → **"Project"**
4. Select your `RIZZA` repository
5. Set **Root Directory** to `frontend`
6. Add environment variable:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://YOUR_RAILWAY_URL.railway.app/api/v1`
7. Click **"Deploy"**
8. Wait for deployment (~2 minutes)
9. Visit your live app URL!

## Verification

1. Visit your Vercel URL
2. Upload a screenshot
3. Generate replies
4. Confirm everything works!

---

**Need help?** Provide me with:
- Your GitHub repository URL
- Any errors you encounter

I'll assist you through each step!
