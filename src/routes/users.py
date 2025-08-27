from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.controllers import notes as notes_contoller
from src.common import db_dependency
from models.user import User
from schemas.users import UserCreate, UserOut
from passlib.context import CryptContext
from src.utility.security import hash_password


router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: db_dependency):
   db_user = db.query(User).filter(User.email == user.email).first()
   if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
   
   new_user = User(
       username=user.username,
       email=user.email,
       hashed_password=hash_password(user.password)
   )
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user





