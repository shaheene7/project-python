from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class GrammarIssueBase(BaseModel):
    revision_id: int
    position: int
    length: int
    issue_type: str
    message: str
    suggestion: Optional[str] = None

class GrammarIssueCreate(GrammarIssueBase):
    pass

class GrammarIssueUpdate(BaseModel):
    position: Optional[int] = None
    length: Optional[int] = None
    issue_type: Optional[str] = None
    message: Optional[str] = None
    suggestion: Optional[str] = None

class GrammarIssueOut(GrammarIssueBase):
    id: int
    created_at: datetime