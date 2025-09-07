from datetime import datetime 
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , TEXT, DateTime
from src.common.connection import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
