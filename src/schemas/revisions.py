from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RevisionBase(BaseModel):
    content: str
    note_id: int


class RevisionCreate(RevisionBase):
    pass

class RevisionOut(RevisionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True