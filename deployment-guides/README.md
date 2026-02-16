# Quick Start - Deploy to Production

This is the fastest way to get your AI Reply Strategist live on the web.

## Prerequisites

- Git repository (GitHub, GitLab, or Bitbucket) with your code
- [Railway account](https://railway.app/) (free)
- [Vercel account](https://vercel.com/) (free)
- OpenAI API key

## Deployment Steps

### 1. Deploy Backend to Railway (~5 minutes)

Follow the detailed guide: [railway.md](./railway.md)

**Quick summary:**
1. Push code to Git
2. Create Railway project from GitHub repo
3. Set root directory to `backend`
4. Add `OPENAI_API_KEY` environment variable
5. Generate domain and copy the URL

### 2. Deploy Frontend to Vercel (~5 minutes)

Follow the detailed guide: [vercel.md](./vercel.md)

**Quick summary:**
1. Update `frontend/.env.production` with your Railway backend URL
2. Push changes to Git
3. Create Vercel project from GitHub repo
4. Set root directory to `frontend`
5. Add `NEXT_PUBLIC_API_URL` environment variable
6. Deploy and visit your live app!

## Result

Your app will be live at:
- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://your-app.railway.app`

## Cost

Both platforms offer generous free tiers:
- **Railway:** $5 credit/month, enough for this app
- **Vercel:** Unlimited for personal projects

Total: **$0/month** for hobby use! 🎉
