from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from src.models.revisions import Revision
from sqlalchemy.orm import Session
import markdown, bleach, hashlib
from src.common.connection import db_dependency

router = APIRouter(prefix="/content", tags=["Content Delivery"])

ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + ["p","pre","code","h1","h2","h3","h4","h5","h6"]

@router.get("/{revision_id}")
def render_content(revision_id: int, request: Request, db: db_dependency):
    revision = db.query(Revision).filter(Revision.id == revision_id).first()
    if not revision:
        raise HTTPException(status_code=404, detail="Revision not found")

    raw_html = markdown.markdown(revision.content)
    safe_html = bleach.clean(raw_html, tags=ALLOWED_TAGS, strip=True)

    etag = hashlib.md5(safe_html.encode("utf-8")).hexdigest()
    if_none_match = request.headers.get("if-none-match")
    if if_none_match == etag:
        return PlainTextResponse(status_code=304, content="")

    accept_header = request.headers.get("accept", "text/html")
    if "application/json" in accept_header:
        response = JSONResponse(content={"html": safe_html})
    elif "text/plain" in accept_header:
        response = PlainTextResponse(content=safe_html)
    else:
        response = HTMLResponse(content=safe_html)

    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "public, max-age=3600"
    return response
