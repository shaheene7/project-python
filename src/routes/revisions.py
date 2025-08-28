from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.common.connection import db_dependency
from models.revisions import Revision
from schemas.revisions import RevisionCreate, RevisionOut


router = APIRouter(prefix="/revisions", tags=["Revisions"])

@router.post("/{user_id}", response_model=RevisionOut)
def create_revision(revision: RevisionCreate, user_id: int ,db: db_dependency):
    new_revision = Revision(
        content=revision.content,
        note_id=revision.note_id,
        created_by=user_id
    )
    db.add(new_revision)
    db.commit()
    db.refresh(new_revision)
    return new_revision


