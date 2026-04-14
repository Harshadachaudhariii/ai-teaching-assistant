# api/user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from services.user_service import get_user_by_id, update_user
from schemas.user_schema import UserResponse, UserUpdateRequest
from dependencies.auth import get_current_user
from models.user import User
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

# -------------------- GET PROFILE --------------------
@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    logger.info(f"[USER API] Profile request | user_id={current_user.id}")
    return current_user


# -------------------- UPDATE PROFILE --------------------
@router.put("/profile")
def update_profile(
    data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"[USER API] Update request | user_id={current_user.id}")

    user, error = update_user(db, current_user.id, data.name, data.email)

    if error:
        logger.warning(f"[USER API] Update failed | {error}")
        raise HTTPException(status_code=400, detail=error)

    logger.info(f"[USER API] Update success | user_id={current_user.id}")
    return {"message": "Profile updated successfully", "user": user}