from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.common.connection import db_dependency
from models.user import User
from schemas.users import UserCreate, UserOut
from starlette import status
from passlib.context import CryptContext
from src.utility.security import hash_password
from src.utility.auth import bcrypt_context


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


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                      create_user_request: UserCreate):
    create_user_model = User(username= create_user_request.username,
                              hashed_password= bcrypt_context.hash(create_user_request.password),
                              email = create_user_request.email)
    
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"msg" : "User created successfully"}





