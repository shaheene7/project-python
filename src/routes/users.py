from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from src.common.connection import db_dependency
from src.models.user import User
from src.schemas.users import UserCreate, UserOut, UserLogin
from starlette import status
from passlib.context import CryptContext
from src.utility.security import hash_password
from src.utility.auth import bcrypt_context, authenticate_user, login_for_access_token, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.token import Token
from src.common.connection import get_db
from src.controllers import users as users_controller
 

router = APIRouter(prefix="/users",tags=["Users"])



@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return await login_for_access_token(form_data, db)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
                      create_user_request: UserCreate,
                      db: Session = Depends(get_db) ):


    return await users_controller.create_user(create_user_request, db)