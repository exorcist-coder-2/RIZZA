from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = relationship("ChatMessage", back_populates="session", order_by="ChatMessage.created_at")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    image_path = Column(String, nullable=True)  # path to attached screenshot
    is_voice = Column(Boolean, default=False)  # was this from a voice note
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


class ContactMemory(Base):
    __tablename__ = "contact_memories"

    id = Column(Integer, primary_key=True, index=True)
    contact_name = Column(String, index=True, nullable=False)
    fact = Column(Text, nullable=False)  # e.g. "Gets anxious when left on read"
    category = Column(String, nullable=True)  # personality, pattern, preference, history
    created_at = Column(DateTime, default=datetime.utcnow)
