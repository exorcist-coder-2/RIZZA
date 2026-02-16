from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.v1.endpoints import (
    analyze_router, 
    reply_router, 
    chat_router, 
    transcribe_router,
    contacts_router
)
from core.database import engine, Base
from models import contact, conversation  # Import models to register them

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(analyze_router, prefix=f"{settings.API_V1_STR}/analyze", tags=["analyze"])
app.include_router(reply_router, prefix=f"{settings.API_V1_STR}/reply", tags=["reply"])
app.include_router(chat_router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(transcribe_router, prefix=f"{settings.API_V1_STR}/transcribe", tags=["transcribe"])
app.include_router(contacts_router, prefix=f"{settings.API_V1_STR}/contacts", tags=["contacts"])

@app.get("/")
async def root():
    return {"message": "AI Reply Strategist API is running"}

# Print registered routes for debugging
@app.on_event("startup")
async def startup_event():
    print("Registered routes:")
    for route in app.routes:
        print(f"Path: {route.path}")
