from sqlalchemy import Column, Integer, String, Date, Text
from core.database import Base
from datetime import date

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    nickname = Column(String, nullable=True)
    relationship_type = Column(String, nullable=True) # Dating, Spouse, etc.
    first_interaction_date = Column(Date, default=date.today)
    notes = Column(Text, nullable=True)
    
    # Emotional data
    emotional_volatility = Column(Integer, default=0) # Index
    responsiveness_score = Column(Integer, default=50) 
