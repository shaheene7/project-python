from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , TEXT, DateTime
from src.common.connection import Base


class Revision(Base):
    __tablename__ = "revisions"

    id = Column(Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False, unique=True)
    revision_number = Column(Integer, nullable=False, unique=True)
    content = Column(TEXT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))