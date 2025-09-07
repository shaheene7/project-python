from datetime import timedelta
from typing import Annotated, Literal
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import Field
from sqlalchemy.orm import Session
from src.models.notes import Note
from src.models.revisions import Revision
from src.models.user import User
from src.schemas.users import UserCreate, UserLogin, UserOut
from src.common.connection import db_dependency
from src.common.connection import get_db
from src.utility.auth import create_access_token, login_for_access_token, bcrypt_context




def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db) 
):
    return login_for_access_token(form_data, db)





async def create_user(create_user_request: UserCreate, 
                      db: Session = Depends(get_db) ):
   
    
    if db.query(User).filter(User.email == create_user_request.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(username= create_user_request.username,
                hashed_password= bcrypt_context.hash(create_user_request.password),
                email = create_user_request.email,
                is_verified=True)
    
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token_expires = timedelta(minutes=20)
    token = create_access_token(
        username=user.username,
        user_id=user.id,
        expires_delta=access_token_expires
    )

    return {
        "msg": "User created successfully",
        "access_token": token,
        "token_type": "bearer"
    }