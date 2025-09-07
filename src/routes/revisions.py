from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.common.connection import db_dependency
from src.models.revisions import Revision
from src.schemas.revisions import RevisionCreate, RevisionOut
from src.controllers import revisions as revisions_controller
from src.utility.auth import get_current_user


router = APIRouter(prefix="/revisions", tags=["Revisions"])

@router.post("/", response_model=RevisionOut)
def create_revision(revision: RevisionCreate, db: db_dependency, current_user = Depends(get_current_user)):
    return revisions_controller.create_revision(revision, current_user.id, db)

@router.get("/" , response_model=List[RevisionOut])
def get_revisions(db: db_dependency, current_user = Depends(get_current_user)):
    return revisions_controller.get_revisions(db)


@router.get("/{revision_id}", response_model=RevisionOut)
def get_revision(revision_id: int, db: db_dependency, current_user = Depends(get_current_user)):
    return revisions_controller.get_revision(revision_id, db)

# @router.put("/{revision_id}", response_model=RevisionOut)
# def update_revision(revision_id: int, revision_update: RevisionCreate, db: db_dependency):
#     revision = db.query(Revision).filter(Revision.id == revision_id).first()

#     if not revision:
#         raise HTTPException(status_code=404, detail="Revision not found")
    

