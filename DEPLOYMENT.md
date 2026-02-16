# Deployment Guide

This guide explains how to deploy the AI Reply Strategist application.

## 🚀 Quick Start - Cloud Deployment (Recommended)

**Deploy to production in under 10 minutes:**

1. **Backend (Railway):** [deployment-guides/railway.md](deployment-guides/railway.md)
2. **Frontend (Vercel):** [deployment-guides/vercel.md](deployment-guides/vercel.md)

Both platforms offer generous free tiers perfect for this application.

---

## 🐳 Docker Deployment (Local/VPS)

- Docker and Docker Compose installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Docker Quick Start

### 1. Set Up Environment Variables

Copy the example environment file and add your Gemini API key:

```bash
cp .env.example .env
```

Edit `.env` and replace `your_openai_api_key_here` with your actual API key:

```
OPENAI_API_KEY=your_actual_api_key_here
```

### 2. Build and Start Services

```bash
docker-compose up --build
```

This will:
- Build the backend (FastAPI) image
- Build the frontend (Next.js) image
- Start both services with proper networking

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Development vs Production Options

### Local Development (without Docker)

**Backend:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Production Deployment

For production deployment to cloud platforms:

#### Option 1: Docker Compose (VPS/Cloud VM)

1. Copy your project to the server
2. Set up `.env` with production API key
3. Run: `docker-compose up -d`

#### Option 2: Separate Deployments

**Backend** (Railway, Render, Fly.io):
- Deploy from `backend/` directory
- Set `GEMINI_API_KEY` environment variable
- Use the Dockerfile

**Frontend** (Vercel, Netlify):
- Deploy from `frontend/` directory
- Set `NEXT_PUBLIC_API_URL` to your backend URL
- Platform will auto-detect Next.js

## Environment Variables

### Backend
- `OPENAI_API_KEY` (required): Your OpenAI API key

### Frontend
- `NEXT_PUBLIC_API_URL` (optional): Backend API URL
  - Default: `http://localhost:8000/api/v1`
  - Docker: `http://backend:8000/api/v1`
  - Production: Set to your deployed backend URL

## Troubleshooting

### Port Already in Use
If ports 3000 or 8000 are already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "3001:3000"  # Change host port
```

### Backend Health Check Fails
Ensure the backend starts successfully by checking logs:

```bash
docker-compose logs backend
```

### Frontend Can't Connect to Backend
- In Docker: Use `http://backend:8000/api/v1`
- Outside Docker: Use `http://localhost:8000/api/v1`

## Stopping Services

```bash
docker-compose down
```

To also remove volumes:

```bash
docker-compose down -v
```

## Database Persistence

The SQLite database is stored in `backend/data/` and persisted via Docker volume mount.
