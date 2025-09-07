from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.controllers import notes as notes_contoller
from src.common.connection import db_dependency
from src.models.notes import Note
from src.schemas.folders import FolderCreate, FolderOut
from src.utility.auth import get_current_user
from src.models.folders import Folder



router = APIRouter(prefix="/folders", tags=["Folders"])

@router.post("/", response_model=FolderOut)
def create_folder(folder: FolderCreate, db: db_dependency, current_user = Depends(get_current_user)):
    new_folder = Folder(name=folder.name, user_id=current_user.id)
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)
    return new_folder

@router.get("/", response_model=list[FolderOut])
def get_folders(db: db_dependency):
    return db.query(Folder).all()