# api/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from services.auth_service import register_user, login_user
from schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse
from dependencies.auth import get_current_user
from models.user import User
from utils.logger import get_logger
from fastapi.security import OAuth2PasswordRequestForm

logger = get_logger(__name__)

router = APIRouter()

# -------------------- REGISTER --------------------
@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    logger.info(f"[AUTH API] Register request | email={data.email}")

    user, error = register_user(db, data.name, data.email, data.password)

    if error:
        logger.warning(f"[AUTH API] Register failed | {error}")
        raise HTTPException(status_code=400, detail=error)

    logger.info(f"[AUTH API] Register success | user_id={user.id}")
    return {"message": "User registered successfully", "user_id": user.id}


# -------------------- LOGIN --------------------
@router.post("/login-form")
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"[AUTH API] Login form request | email={form_data.username}")

    result, error = login_user(db, form_data.username, form_data.password)

    if error:
        logger.warning(f"[AUTH API] Login failed | {error}")
        raise HTTPException(status_code=401, detail=error)

    logger.info(f"[AUTH API] Login success | user_id={result['user_id']}")
    return result


# -------------------- ME --------------------
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    logger.info(f"[AUTH API] Me request | user_id={current_user.id}")
    return {
        "user_id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "created_at": current_user.created_at
    }