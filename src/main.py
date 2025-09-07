# from fastapi import FastAPI, HTTPException ,status
# from fastapi.middleware.cors import CORSMiddleware

# from src.routes import notes, users, revisions
# from common.connection import Base, engine, db_dependency

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# def start_server():

#     app.include_router(notes.router)
#     app.include_router(users.router)
#     app.include_router(revisions.router)


