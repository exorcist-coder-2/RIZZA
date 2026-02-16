# Railway Deployment - Step by Step

Your code is now on GitHub! Let's deploy the backend to Railway.

## Repository URL
✅ https://github.com/exorcist-coder-2/RIZZA

## Step 1: Deploy Backend to Railway

### 1.1 Sign Up / Sign In to Railway
1. Go to https://railway.app/
2. Click **"Login"** or **"Start a New Project"**
3. Sign in with GitHub (recommended for easy integration)
4. Authorize Railway to access your GitHub account

### 1.2 Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find and select **"exorcist-coder-2/RIZZA"**
4. Railway will automatically start deploying

### 1.3 Configure the Backend Service
1. Click on the created service (it will show up as a card)
2. Go to **Settings** tab
3. Scroll to **"Source"** section
4. Click **"Change"** next to **Root Directory**
5. Enter: `backend`
6. Click **"Update"**

### 1.4 Add Environment Variables
1. Go to the **Variables** tab
2. Click **"+ New Variable"**
3. Add your OpenAI API key:
   - **Name:** `OPENAI_API_KEY`
   - **Value:** `your_actual_openai_api_key_here`
4. Click **"Add"**

> **Note:** The `PORT` variable is automatically provided by Railway

### 1.5 Generate Public Domain
1. Go to **Settings** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"** under **Public Networking**
4. Railway will generate a URL like: `https://rizza-production-xxxx.railway.app`
5. **COPY THIS URL** - you'll need it for the frontend!

### 1.6 Verify Deployment
1. Wait for the build to complete (~2-3 minutes)
2. Visit your Railway domain URL
3. You should see: `{"message": "AI Reply Strategist API is running"}`
4. Visit `/docs` endpoint: `https://your-railway-url.railway.app/docs`
5. You should see the FastAPI Swagger documentation

## Troubleshooting

**Build Failed?**
- Check the **Deployments** tab for build logs
- Common issues:
  - Missing dependencies (should be in requirements.txt)
  - Docker build errors (check Dockerfile syntax)

**App Crashes?**
- Check **Deployments** → **Logs**
- Common issues:
  - Missing `OPENAI_API_KEY` environment variable
  - Port binding issues (Railway auto-provides `$PORT`)

**Health Check Fails?**
- The app must respond to `/` within 100 seconds
- Check logs to see if the app is starting

---

## ✅ Once Backend is Deployed

Copy your Railway backend URL (e.g., `https://rizza-production-xxxx.railway.app`) and proceed to the next step: deploying the frontend to Vercel.

**Your Railway Backend URL:** _______________________________

Save this URL - you'll need it for the frontend deployment!
