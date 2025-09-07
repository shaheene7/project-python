from datetime import datetime
import enum
from typing import Optional
from pydantic import BaseModel

class IssueTypeEnum(str, enum.Enum):
    spelling = "spelling"
    grammar = "grammar"
    punctuation = "punctuation"
    style = "style"

    
class GrammarIssueBase(BaseModel):
    revision_id: int
    position: int
    length: int
    issue_type: IssueTypeEnum
    suggestion: Optional[str] = None
    message: Optional[str] = None
    

class GrammarIssueCreate(GrammarIssueBase):
    pass

class GrammarIssueUpdate(BaseModel):
    position: Optional[int] = None
    length: Optional[int] = None
    issue_type: Optional[IssueTypeEnum] = None
    message: Optional[str] = None
    suggestion: Optional[str] = None

class GrammarIssueOut(GrammarIssueBase):
    id: int
    created_at: datetime