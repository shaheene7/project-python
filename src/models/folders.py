from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , TEXT, DateTime
from src.common.connection import Base


class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)