from typing import Annotated, Literal
from fastapi import HTTPException
from pydantic import Field
from sqlalchemy.orm import Session
from src.models.notes import Note
from src.models.grammar_issues import GrammarIssue
from src.models.revisions import Revision
from src.schemas.grammar_issues import GrammarIssueCreate, GrammarIssueOut, GrammarIssueUpdate 
from src.common.connection import db_dependency


def create_grammar_issue(issue: GrammarIssueCreate, db:db_dependency):
    db_issue = GrammarIssue(
        revision_id = issue.revision_id,
        position = issue.position,
        length = issue.length,
        issue_type = issue.issue_type,
        suggestion = issue.suggestion,
        message = issue.message
    )

    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def get_grammar_issues(db: db_dependency):
    grammar_issues = db.query(GrammarIssue).all()

    if not grammar_issues:
        raise HTTPException(status_code=404, detail="No grammar issues found")
    return grammar_issues


def accept_grammar_issue(issue_id: int, db: db_dependency,  user_id: int):

    db_issue = db.query(GrammarIssue).filter(GrammarIssue.id == issue_id).first()

    if not db_issue:
        raise HTTPException(status_code=404, detail="Grammar issue not found")
    
    db_revision = db.query(Revision).filter(Revision.id == db_issue.revision_id).first()

    if not db_revision:
        raise HTTPException(status_code=404, detail="Revision not found")

    before = db_revision.content[:db_issue.position]
    after = db_revision.content[db_issue.position + db_issue.length:]
    new_content = before + db_issue.suggestion + after

    last_revision = (
        db.query(Revision)
        .filter(Revision.note_id == db_revision.note_id)
        .order_by(Revision.revision_number.desc())
        .first()
    )
    next_revision_number = 1 if not last_revision else last_revision.revision_number + 1

    revision = Revision(
        content = new_content,
        revision_number=next_revision_number,
        note_id = db_revision.note_id,
        created_by = user_id

    )
    db.add(revision)
    db.commit()
    db.refresh(db_issue)
    db.refresh(revision)
    return db_issue


def accept_issues(db: Session, revision_id: int, issue_ids: list[int], user_id: int):

    db_revision = db.query(Revision).filter(Revision.id == revision_id).first()
    if not db_revision:
        raise HTTPException(status_code=404, detail="Revision not found")

    
    db_issues = (
        db.query(GrammarIssue)
        .filter(GrammarIssue.revision_id == revision_id, GrammarIssue.id.in_(issue_ids))
        .all()
    )
    if not db_issues:
        raise HTTPException(status_code=404, detail="No valid issues found")
    
    db_issues.sort(key=lambda x: x.position, reverse=True)

   
    new_content = db_revision.content


    for issue in db_issues:
        before = new_content[:issue.position]
        after = new_content[issue.position + issue.length :]
        new_content = before + issue.suggestion + after

    last_revision = (
        db.query(Revision)
        .filter(Revision.note_id == db_revision.note_id)
        .order_by(Revision.revision_number.desc())
        .first()
    )
    
    next_revision_number = 1 if not last_revision else last_revision.revision_number + 1
        
    new_revision = Revision(
        content = new_content,
        revision_number=next_revision_number,
        note_id = db_revision.note_id,
        created_by = user_id

    )
    db.add(new_revision)
    db.commit()
    db.refresh(new_revision)

    return new_revision
