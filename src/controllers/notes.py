from typing import Annotated, Literal
from fastapi import HTTPException
from pydantic import Field
from sqlalchemy.orm import Session
from src.models.notes import Note
from src.models.revisions import Revision
from src.schemas.notes import NoteCreate, NoteUpdate
from src.common.connection import db_dependency
from src.models.folders import Folder

def create_note(note: NoteCreate, user_id:int ,db: db_dependency):

    folder = db.query(Folder).filter(Folder.id == note.folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found, you can not add note to non existing folder")
    

    

    db_note = Note(
        title = note.title,
        user_id = user_id,
        folder_id = note.folder_id,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    last_revision = (
        db.query(Revision)
        .filter(Revision.note_id == db_note.id)
        .order_by(Revision.revision_number.desc())
        .first()
    )

    next_revision_number = 1 if last_revision is None else last_revision.revision_number + 1

    new_revision = Revision(
        content=note.content,
        note_id=db_note.id,
        created_by=user_id,
        revision_number=next_revision_number
    )
    return db_note

def get_notes(db:db_dependency):
     return db.query(Note).filter(Note.is_deleted == False).all()


def get_note(note_id: int, db: db_dependency):
    db_note = db.query(Note).filter(Note.id == note_id, Note.is_deleted == False).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


def update_note(note_id: int, note_update: NoteUpdate, db: db_dependency, user_id:int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    last_revision = (
        db.query(Revision)
        .filter(Revision.note_id == note.id)
        .order_by(Revision.revision_number.desc())
        .first()
    )
    next_revision_number = 1 if not last_revision else last_revision.revision_number + 1

    
    revision = Revision(
        note_id=note.id,
        revision_number=next_revision_number,
        content=note_update.content,
        created_by=user_id
    )
    db.add(revision)

   
    if note_update.title is not None:
        note.title = note_update.title
    if note_update.folder_id is not None:
        folder = db.query(Folder).filter(Folder.id == note_update.folder_id).first()
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found, you can not move note to non existing folder")
        note.folder_id = note_update.folder_id
    if note_update.tags is not None:
        note.tags = note_update.tags
    if note_update.is_deleted is not None:
        note.is_deleted = note_update.is_deleted
    
        
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


def restore_note(note_id: int, db: db_dependency, revision_id: int, user_id: int):
    note = db.query(Note).filter(Note.id == note_id, Note.is_deleted == False).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    

    if revision_id:
        revision = db.query(Revision).filter(
        Revision.id == revision_id,
        Revision.note_id == note_id
        ).first()
        if not revision:
            raise HTTPException(status_code=404, detail="Revision not found")
    else:
        revision = db.query(Revision).filter(Revision.note_id == note.id).order_by(Revision.revision_number.desc()).offset(1).first()
        if not revision:
            raise HTTPException(status_code=400, detail="No previous revision to restore")    
        
    last_revision = (
        db.query(Revision)
        .filter(Revision.note_id == note.id)
        .order_by(Revision.revision_number.desc())
        .offset(1)
        .first()
    )

    next_revision_number = 1 if not last_revision else last_revision.revision_number + 1

    revision = Revision(
        note_id=note.id,
        revision_number=next_revision_number,
        content=revision.content,
        created_by=user_id
    )
    db.add(revision)
    db.commit()
    db.refresh(revision)
    return revision

def get_notes_by_folders(folder_id: int, db: db_dependency):
    notes = db.query(Note).filter(Note.folder_id == folder_id, Note.is_deleted == False).all()
    if not notes:
        raise HTTPException(status_code=404, detail="No notes found in this folder")
    return notes