from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    folder_id: int | None = None
    tags: Optional[list[str]] = None

class NoteCreate(NoteBase):
    content: str

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    folder_id: Optional[int] = None
    tags: Optional[list[str]] = None
    is_deleted: Optional[bool] = None



class NoteOut(NoteBase):
    id: int
    user_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  