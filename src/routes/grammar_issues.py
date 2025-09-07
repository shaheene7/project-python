from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.common.connection import db_dependency
from src.models.revisions import Revision
from src.schemas.revisions import RevisionOut
from src.schemas.grammar_issues import GrammarIssueCreate, GrammarIssueOut
from src.controllers import grammar_issues as grammar_issues_controller
from src.utility.auth import get_current_user



router = APIRouter(prefix="/grammar-issues", tags=["Grammar Issues"])


@router.post("/", response_model=GrammarIssueOut)
async def create_grammar_issue(issue: GrammarIssueCreate, db: db_dependency, current_user = Depends(get_current_user)):
    return await grammar_issues_controller.create_grammar_issue(issue, db)


@router.get("/", response_model=List[GrammarIssueOut])
async def get_grammar_issues(db: db_dependency, current_user = Depends(get_current_user)):
    return await grammar_issues_controller.get_grammar_issues(db)


@router.post("/{issue_id}/accept", response_model=GrammarIssueOut)
async def accept_grammar_issue(issue_id: int, db: db_dependency, current_user = Depends(get_current_user)):
    return await grammar_issues_controller.accept_grammar_issue(issue_id, db)


@router.post("/accept", response_model=RevisionOut)
async def accept_grammar_issues(issue_ids: List[int], db: db_dependency, current_user = Depends(get_current_user)):
    return await grammar_issues_controller.accept_grammar_issues(issue_ids, db)