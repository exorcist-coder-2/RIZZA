from api.v1.endpoints.analyze import router as analyze_router
from api.v1.endpoints.reply import router as reply_router
from api.v1.endpoints.chat import router as chat_router
from api.v1.endpoints.transcribe import router as transcribe_router
from api.v1.endpoints.contacts import router as contacts_router

__all__ = [
    "analyze_router",
    "reply_router",
    "chat_router",
    "transcribe_router",
    "contacts_router"
]
