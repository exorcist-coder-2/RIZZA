# Railway Deployment Guide - Backend

Deploy the AI Reply Strategist backend to Railway in under 5 minutes.

## Prerequisites

- [Railway account](https://railway.app/) (free tier available)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git repository (GitHub, GitLab, or Bitbucket)

## Step 1: Prepare Your Repository

Make sure your code is pushed to a Git repository:

```bash
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

## Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app/) and sign in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your repositories
5. Select your **RIZZA** repository

## Step 3: Configure the Project

Railway will auto-detect the Dockerfile. Configure it:

1. **Set Root Directory:**
   - Click on your service
   - Go to **Settings** → **Service Settings**
   - Set **Root Directory** to `backend`
   - Click **Save**

2. **Add Environment Variables:**
   - Go to the **Variables** tab
   - Click **"+ New Variable"**
   - Add: `OPENAI_API_KEY` = `your_actual_openai_api_key`
   - Railway automatically provides `PORT` variable

3. **Configure Build:**
   - Railway will use the `railway.json` in your root
   - No additional configuration needed

## Step 4: Deploy

1. Railway will automatically start building
2. Wait for deployment to complete (~2-3 minutes)
3. Once deployed, you'll see a **"Deployments"** section with a green checkmark

## Step 5: Get Your Backend URL

1. In your service, go to **Settings** → **Networking**
2. Click **"Generate Domain"**
3. Copy the generated URL (e.g., `https://your-app-name.railway.app`)
4. **Save this URL** - you'll need it for frontend deployment

## Step 6: Verify Deployment

Visit your backend URL:

- **API Root:** `https://your-app-name.railway.app/`
  - Should return: `{"message": "AI Reply Strategist API is running"}`

- **API Documentation:** `https://your-app-name.railway.app/docs`
  - FastAPI Swagger UI should load

## Troubleshooting

### Build Fails

**Check build logs:**
1. Click on your service
2. Go to **Deployments** tab
3. Click on the failed deployment
4. Review logs for errors

**Common issues:**
- Missing dependencies in `requirements.txt`
- Docker build errors - verify `backend/Dockerfile` syntax

### Deployment Succeeds but App Crashes

**Check runtime logs:**
1. Go to **Deployments** → Click active deployment
2. Check logs for Python errors

**Common issues:**
- Missing `OPENAI_API_KEY` environment variable
- Database connection issues (Railway provides volume mounting)

### Health Check Fails

The app must respond to `/` within 100 seconds:
- Check that FastAPI is starting properly
- Verify `curl` is installed in Dockerfile (already added)

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `PORT` | Auto | Railway auto-provides this |

## Updating Your Deployment

Railway auto-deploys on every push to your main branch:

```bash
# Make changes
git add .
git commit -m "Update backend"
git push origin main
# Railway automatically rebuilds and redeploys
```

## Next Steps

✅ Backend deployed! Now deploy the frontend:
- Follow [vercel.md](./vercel.md) to deploy the frontend
- Use the Railway backend URL you copied in Step 5
