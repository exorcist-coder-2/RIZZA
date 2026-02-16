from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.contact import Contact
from core.database import get_db
from pydantic import BaseModel
from datetime import date

router = APIRouter()

# Pydantic models (should ideally be in separate schemas file)
class ContactCreate(BaseModel):
    name: str
    nickname: str | None = None
    relationship_type: str | None = None
    notes: str | None = None

class ContactResponse(ContactCreate):
    id: int
    first_interaction_date: date | None = None
    emotional_volatility: int
    responsiveness_score: int

    class Config:
        orm_mode = True

@router.post("/", response_model=ContactResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/", response_model=List[ContactResponse])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
