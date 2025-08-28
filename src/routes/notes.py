from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.controllers import notes as notes_contoller
from src.common.connection import db_dependency
from models import Note
from schemas import NoteCreate, NoteUpdate, NoteOut


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/{user_id}", response_model=NoteOut)
def create_note(note: NoteCreate, user_id:int ,db: db_dependency):
  return notes_contoller.create_note(note, user_id ,db)

@router.get("/", response_model=list[NoteOut])
def get_notes(db: db_dependency):
    return notes_contoller.get_notes(db)


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: db_dependency):
  return notes_contoller.get_note(note_id, db)


@router.put("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note_update: NoteUpdate, db: db_dependency):
  return notes_contoller.update_note(note_id, note_update, db)

@router.delete("/{note_id}")
def delete_note(note_id: int, db: db_dependency):
   return notes_contoller.delete_note(note_id, db)