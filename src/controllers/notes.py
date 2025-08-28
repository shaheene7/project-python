from typing import Annotated, Literal
from fastapi import HTTPException
from pydantic import Field
from sqlalchemy.orm import Session
from models.notes import Note
from schemas.notes import NoteCreate, NoteOut, NoteUpdate
from src.common.connection import db_dependency

def create_note(note: NoteCreate, db: db_dependency):
    db_note = Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes(db:db_dependency):
     return db.query(Note).filter(Note.is_deleted == False).all()



def get_note(note_id: int, db: db_dependency):
    db_note = db.query(Note).filter(Note.id == note_id, Note.is_deleted == False).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


def update_note(note_id: int, note_update: NoteUpdate, db: db_dependency):
    note = db.query(Note).filter(Note.id == note_id, Note.is_deleted == False).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note_update.title is not None:
        note.title = note_update.title

    db.commit()
    db.refresh(note)
    return note


def delete_note(note_id: int, db: db_dependency):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.is_deleted = True  
    db.commit()
    return {"message": "Note deleted successfully"}
