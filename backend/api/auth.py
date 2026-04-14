from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from services.auth_service import register_user, login_user
from pydantic import BaseModel


router = APIRouter()

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user, error = register_user(db, data.name, data.email, data.password)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "User registered successfully", "user_id": user.id}

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    result, error = login_user(db, data.email, data.password)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return result

