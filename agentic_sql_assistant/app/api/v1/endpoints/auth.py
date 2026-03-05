from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.services.database import get_session, db_service
from app.core import security
from app.models.user import User
from app.models.session import Session as ChatSession
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=User)
def register(user_in: UserCreate, session: Session = Depends(get_session)) -> Any:
    user = db_service.get_user_by_email(session, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    user = db_service.create_user(session, user)
    return user

@router.post("/login", response_model=Token)
def login(
    session: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = db_service.get_user_by_email(session, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=60 * 24 * 8) # 8 days
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
