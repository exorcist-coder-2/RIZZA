# AI Reply Strategist

## Tech Stack
- **Backend**: Python FastAPI, OpenAI GPT-4o, SQLAlchemy (SQLite/Postgres)
- **Frontend**: Next.js 14, Tailwind CSS, Lucide React

## Setup Instructions

### Backend
1. Navigate to `backend` directory:
   ```bash
   cd backend
   ```
2. Create virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt 
   # (Or: pip install fastapi uvicorn google-generativeai python-multipart python-dotenv sqlalchemy greenlet pillow)
   ```
3. Set your Gemini API Key in `.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
4. Run the server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at `http://localhost:8000`. Documentation at `/docs`.

### Frontend
1. Navigate to `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies (if not already done):
   ```bash
   npm install
   npm install lucide-react clsx tailwind-merge class-variance-authority @radix-ui/react-slot
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000`.

## Features Implemented (MVP Phase 1)
- **Screenshot Analysis**: Upload chat screenshots to extract conversation and emotion.
- **3-Tone Replies**: Generates Warm, Playful, and Direct reply suggestions.
- **Contact Memory**: Database schema and API for storing contact relationships.

## Notes
- The frontend installation might take a few minutes on the first run.
- Ensure the backend is running before using the frontend.
