from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import folder
from src.models.user import User
from src.models.folders import Folder
from src.models.notes import Note
from src.models.revisions import Revision
from src.models.grammar_issues import GrammarIssue
from src.common.connection import Base, engine
# Import your routers
from src.routes import notes as notes_controller
from src.routes import revisions as revisions_controller
from src.routes import users as user_controller
from src.routes import grammar_issues as grammar_issues_controller
from src.routes import content_delivery
from src.models.user import Base
from src.common.connection import engine




Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI(
    title="Notes & Revision API",
    description="API for Notes, Revisions, Grammar Audit, and Rendered Content",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router)
app.include_router(notes_controller.router)
app.include_router(revisions_controller.router)
app.include_router(grammar_issues_controller.router)
app.include_router(content_delivery.router)
app.include_router(folder.router)


@app.get("/")
def root():
    return {"message": "Notes & Revisions API is running 🚀"}
