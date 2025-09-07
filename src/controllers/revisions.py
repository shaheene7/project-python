from typing import Annotated, Literal
from fastapi import HTTPException
from pydantic import Field
from sqlalchemy.orm import Session
from src.models.notes import Note
from src.models.revisions import Revision
from src.schemas.revisions import RevisionCreate, RevisionOut
from src.common.connection import db_dependency



def create_revision(revision: RevisionCreate, user_id: int ,db: db_dependency):

    last_revision = (
        db.query(Revision)
        .filter(Revision.note_id == revision.note_id)
        .order_by(Revision.revision_number.desc())
        .first()
    )

    next_revision_number = 1 if not last_revision else last_revision.revision_number + 1

    new_revision = Revision(
        revision_number=next_revision_number,
        content=revision.content,
        note_id=revision.note_id,
        created_by=user_id
    )
    db.add(new_revision)
    db.commit()
    db.refresh(new_revision)
    return new_revision



def get_revisions(db: db_dependency):
    return db.query(Revision).all()


def get_revision(revision_id: int, db: db_dependency):
    revision = db.query(Revision).filter(Revision.id == revision_id).first()
    if not revision:
        raise HTTPException(status_code=404, detail="Revision not found")
    return revision