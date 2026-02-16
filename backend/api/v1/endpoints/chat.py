from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from services.chat_service import chat_service
from typing import Optional

router = APIRouter()


@router.post("/")
async def send_message(
    message: str = Form(""),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    """Send a chat message with optional image attachment."""
    if not message and not image:
        raise HTTPException(status_code=400, detail="Must provide a message or image")

    image_bytes = None
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Attachment must be an image")
        image_bytes = await image.read()

    result = await chat_service.send_message(db, message, image_bytes)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result


@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    """Get chat message history."""
    return {"messages": chat_service.get_history(db)}


@router.delete("/")
def clear_chat(db: Session = Depends(get_db)):
    """Clear all chat history."""
    chat_service.clear_history(db)
    return {"message": "Chat history cleared"}
