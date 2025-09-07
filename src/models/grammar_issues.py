from datetime import datetime
import enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , TEXT, DateTime, Enum
from src.common.connection import Base


class GrammarIssue(Base):
    __tablename__ = "grammar_issues"

    id = Column(Integer, primary_key=True)
    revision_id = Column(Integer, ForeignKey("revisions.id", ondelete="CASCADE"))
    position = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    issue_type = Column(Enum("spelling", "grammar", "punctuation", "style", name="issue_types"), nullable=False)
    message = Column(String)
    suggestion = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    