# Vercel Deployment - Step by Step

Deploy the frontend to Vercel after your Railway backend is live.

## Prerequisites
✅ Backend deployed to Railway
🔑 Railway backend URL (from previous step)

## Step 1: Update Frontend Environment

Before deploying to Vercel, update your production environment file with the Railway backend URL.

1. Open `frontend/.env.production`
2. Replace the placeholder with your actual Railway URL:
   ```env
   NEXT_PUBLIC_API_URL=https://YOUR-RAILWAY-URL.railway.app/api/v1
   ```
   Example:
   ```env
   NEXT_PUBLIC_API_URL=https://rizza-production-a1b2.railway.app/api/v1
   ```

3. Commit and push the change:
   ```bash
   git add frontend/.env.production
   git commit -m "Update production API URL with Railway backend"
   git push origin main
   ```

## Step 2: Deploy to Vercel

### 2.1 Sign Up / Sign In to Vercel
1. Go to https://vercel.com/
2. Click **"Sign Up"** or **"Login"**
3. Sign in with GitHub (recommended)
4. Authorize Vercel to access your GitHub account

### 2.2 Import Project
1. Click **"Add New..."** → **"Project"**
2. Find and select **"exorcist-coder-2/RIZZA"**
3. Click **"Import"**

### 2.3 Configure Project
1. **Framework Preset:** Should auto-detect "Next.js" ✓
2. **Root Directory:** 
   - Click **"Edit"**
   - Enter: `frontend`
   - Click **"Continue"**

3. **Build and Output Settings:** (auto-configured, verify)
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

4. **Environment Variables:**
   - Click **"Add"** under Environment Variables
   - **Name:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://YOUR-RAILWAY-URL.railway.app/api/v1`
   - Click **"Add"**

### 2.4 Deploy
1. Click **"Deploy"**
2. Vercel will build and deploy your frontend (~2-3 minutes)
3. Watch the build logs for any errors
4. Once complete, you'll see a success screen with confetti! 🎉

### 2.5 Get Your Live URL
1. Vercel will show your deployment URL
2. Format: `https://rizza-xxxxx.vercel.app` or `https://rizza-exorcist-coder-2.vercel.app`
3. Click **"Visit"** or copy the URL

## Step 3: Test Your Live App

1. Visit your Vercel URL
2. Test the following:
   - ✅ Homepage loads
   - ✅ Upload a screenshot
   - ✅ Generate AI replies
   - ✅ All 3 tone options appear
   - ✅ No console errors

## Troubleshooting

**Build Fails?**
- Check the build logs in Vercel dashboard
- Common issues:
  - TypeScript errors
  - Missing dependencies
  - Node version mismatch

**Frontend Loads but Can't Connect to Backend?**
1. Check browser console for errors
2. Verify `NEXT_PUBLIC_API_URL` is set correctly in Vercel
3. Verify Railway backend is running
4. Remember: Environment variables need **redeploy** to take effect

**To Redeploy:**
1. Go to **Deployments** tab
2. Click **⋮** on latest deployment
3. Click **"Redeploy"**

**CORS Errors?**
- Backend has `allow_origins=["*"]` by default
- Should work with any Vercel domain
- Check Railway logs for CORS-related errors

## Environment Variables Reference

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://YOUR-RAILWAY-URL.railway.app/api/v1` |

⚠️ **Important:** Environment variables starting with `NEXT_PUBLIC_` are embedded at **build time**. After changing them, you must **redeploy**!

---

## ✅ Deployment Complete!

Your app is now live! 🚀

- **Frontend:** `https://rizza-xxxxx.vercel.app`
- **Backend:** `https://rizza-production-xxxx.railway.app`

Share your app with friends and start getting AI-powered reply suggestions!

### Automatic Deployments

Both Railway and Vercel will automatically redeploy when you push to your main branch:

```bash
# Make changes
git add .
git commit -m "Your changes"
git push origin main
# Railway and Vercel automatically rebuild and deploy!
```

### Optional: Custom Domain

**Railway:**
- Settings → Networking → Custom Domain

**Vercel:**
- Settings → Domains → Add domain
