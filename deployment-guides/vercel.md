# Vercel Deployment Guide - Frontend

Deploy the AI Reply Strategist frontend to Vercel in under 5 minutes.

## Prerequisites

- [Vercel account](https://vercel.com/) (free tier available)
- Backend deployed to Railway (see [railway.md](./railway.md))
- Backend URL from Railway (e.g., `https://your-app.railway.app`)
- Git repository

## Step 1: Update Environment Variables

Before deploying, update the production environment file with your Railway backend URL:

1. Open `frontend/.env.production`
2. Replace the placeholder URL:
   ```env
   NEXT_PUBLIC_API_URL=https://your-actual-backend.railway.app/api/v1
   ```
3. Save and commit:
   ```bash
   git add frontend/.env.production
   git commit -m "Update production API URL"
   git push origin main
   ```

## Step 2: Create Vercel Project

1. Go to [vercel.com](https://vercel.com/) and sign in
2. Click **"Add New"** → **"Project"**
3. Import your Git repository (authorize Vercel if needed)
4. Select your **RIZZA** repository

## Step 3: Configure Project

Vercel auto-detects Next.js projects:

1. **Framework Preset:** Should auto-select "Next.js" ✓

2. **Root Directory:**
   - Click **"Edit"** next to Root Directory
   - Enter: `frontend`
   - Click **Save**

3. **Build Settings:** (auto-configured, verify)
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

4. **Environment Variables:**
   - Click **"Environment Variables"**
   - Add variable:
     - **Name:** `NEXT_PUBLIC_API_URL`
     - **Value:** `https://your-backend.railway.app/api/v1` (your Railway URL)
   - Click **Add**

## Step 4: Deploy

1. Click **"Deploy"**
2. Vercel will build and deploy (~2-3 minutes)
3. Wait for the success screen with confetti 🎉

## Step 5: Get Your Frontend URL

1. After deployment, Vercel shows your live URL
2. Default format: `https://rizza-username.vercel.app`
3. Click **"Visit"** to open your app

## Step 6: Verify Deployment

Test your deployed application:

1. **Homepage loads** ✓
2. **Upload a screenshot** - test file upload
3. **Generate replies** - verify backend connection
4. **Check browser console** - should have no errors

If you see errors like "Failed to fetch" or CORS errors:
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check Railway backend is running

## Custom Domain (Optional)

Add your own domain:

1. In your Vercel project, go to **Settings** → **Domains**
2. Enter your domain name
3. Follow DNS configuration instructions
4. Wait for DNS propagation (~5-30 minutes)

## Troubleshooting

### Build Fails

**Check build logs:**
- Vercel shows logs during deployment
- Common issues:
  - Missing dependencies in `package.json`
  - TypeScript errors
  - Missing environment variables

**Fix:**
```bash
# Test build locally first
cd frontend
npm run build
# Fix any errors, then commit and push
```

### API Connection Fails

**Symptoms:**
- "Failed to fetch" errors
- Network errors in browser console
- No replies generated

**Solutions:**

1. **Verify environment variable:**
   - Go to Vercel project **Settings** → **Environment Variables**
   - Check `NEXT_PUBLIC_API_URL` is set correctly
   - Format: `https://your-backend.railway.app/api/v1` (no trailing slash)

2. **Verify backend is running:**
   - Visit your Railway backend URL
   - Should see: `{"message": "AI Reply Strategist API is running"}`

3. **Check CORS:**
   - Backend has `allow_origins=["*"]` by default
   - This allows all origins including Vercel

4. **Redeploy if needed:**
   - After fixing env variables, trigger redeploy:
   - **Deployments** tab → **⋮** → **Redeploy**

### Environment Variables Not Working

Environment variables starting with `NEXT_PUBLIC_` are embedded at **build time**.

**If you change them:**
1. Update in Vercel dashboard
2. **Redeploy** (changes won't apply automatically)

## Environment Variables Reference

| Variable | Required | Example |
|----------|----------|---------|
| `NEXT_PUBLIC_API_URL` | Yes | `https://rizza.railway.app/api/v1` |

## Updating Your Deployment

Vercel auto-deploys on every push to your main branch:

```bash
# Make changes
git add .
git commit -m "Update frontend"
git push origin main
# Vercel automatically rebuilds and redeploys
```

### Preview Deployments

Vercel creates preview deployments for non-main branches:
- Create a branch: `git checkout -b feature/new-ui`
- Push: `git push origin feature/new-ui`
- Vercel creates a preview URL for testing

## Production Checklist

Before sharing your app:

- [ ] Test file upload with real screenshots
- [ ] Verify all 3 reply tones generate correctly
- [ ] Test on mobile device
- [ ] Check all pages load without errors
- [ ] Verify backend API key is valid
- [ ] (Optional) Add custom domain

## Next Steps

✅ **Deployment Complete!** Your app is live at:
- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://your-app.railway.app`

Share your app URL and start getting AI-powered reply suggestions! 🚀
