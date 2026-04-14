# dependencies/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.database import get_db
from core.security import decode_access_token
from models.user import User
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- OAUTH2 SCHEME --------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-form")
# -------------------- GET CURRENT USER --------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    logger.info("[AUTH DEP] Verifying token...")

    # Step 1: Decode token
    payload = decode_access_token(token)

    if payload is None:
        logger.warning("[AUTH DEP] Invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 2: Get user_id from payload
    user_id = payload.get("user_id")

    if not user_id:
        logger.warning("[AUTH DEP] Token missing user_id")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing user information",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 3: Fetch user from DB
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.warning(f"[AUTH DEP] User not found | user_id={user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"[AUTH DEP] Token valid | user_id={user_id} email={user.email}")
    return user