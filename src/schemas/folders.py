from datetime import datetime
from typing import Optional
from pydantic import BaseModel



class FolderBase(BaseModel):
    name : str



class FolderCreate(FolderBase):
   pass

class FolderOut(FolderBase):
    id: int
    user_id: int
    created_at: datetime