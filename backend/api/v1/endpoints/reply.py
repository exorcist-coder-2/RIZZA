from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.llm_service import llm_service
from typing import List, Dict, Any

router = APIRouter()

class ConversationContext(BaseModel):
    conversation: List[Dict[str, Any]]
    summary: str
    overall_mood: str
    participant_name: str

@router.post("/")
async def generate_reply(context: ConversationContext):
    result = await llm_service.generate_replies(context.dict())
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result
