from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.controllers import notes as notes_contoller
from src.common.connection import db_dependency
from src.models.notes import Note
from src.schemas.notes import NoteCreate, NoteUpdate, NoteOut
from src.utility.auth import get_current_user


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=NoteOut)
def create_note(note: NoteCreate, db: db_dependency,  current_user = Depends(get_current_user)):
  return notes_contoller.create_note(note, current_user.id ,db)

@router.get("/", response_model=list[NoteOut])
def get_notes(db: db_dependency, current_user = Depends(get_current_user)):
    return notes_contoller.get_notes(db)


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: db_dependency, current_user = Depends(get_current_user)):
  return notes_contoller.get_note(note_id, db)


@router.put("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note_update: NoteUpdate, db: db_dependency, current_user = Depends(get_current_user)):
  return notes_contoller.update_note(note_id, note_update, db, current_user.id)

@router.delete("/{note_id}")
def delete_note(note_id: int, db: db_dependency, current_user = Depends(get_current_user)):
   return notes_contoller.delete_note(note_id, db)


@router.get("/folder/{folder_id}", response_model=list[NoteOut])
def get_notes_by_folders(folder_id: int, db: db_dependency, current_user = Depends(get_current_user)):
   return notes_contoller.get_notes_by_folders(folder_id, db)