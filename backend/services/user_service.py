# services/user_service.py

from sqlalchemy.orm import Session
from models.user import User
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- GET USER BY ID --------------------
def get_user_by_id(db: Session, user_id: int):
    logger.info(f"[USER SERVICE] Fetching user | user_id={user_id}")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.warning(f"[USER SERVICE] User not found | user_id={user_id}")
        return None, "User not found"

    logger.info(f"[USER SERVICE] User found | email={user.email}")
    return user, None


# -------------------- GET USER BY EMAIL --------------------
def get_user_by_email(db: Session, email: str):
    logger.info(f"[USER SERVICE] Fetching user | email={email}")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        logger.warning(f"[USER SERVICE] User not found | email={email}")
        return None, "User not found"

    logger.info(f"[USER SERVICE] User found | email={user.email}")
    return user, None


# -------------------- UPDATE USER --------------------
def update_user(db: Session, user_id: int, name: str = None, email: str = None):
    logger.info(f"[USER SERVICE] Update request | user_id={user_id}")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.warning(f"[USER SERVICE] User not found | user_id={user_id}")
        return None, "User not found"

    # Update only provided fields
    if name:
        user.name = name
        logger.info(f"[USER SERVICE] Name updated | user_id={user_id}")

    if email:
        # Check if email already taken
        existing = db.query(User).filter(User.email == email).first()
        if existing and existing.id != user_id:
            logger.warning(f"[USER SERVICE] Email already taken | email={email}")
            return None, "Email already taken"
        user.email = email
        logger.info(f"[USER SERVICE] Email updated | user_id={user_id}")

    db.commit()
    db.refresh(user)

    logger.info(f"[USER SERVICE] User updated successfully | user_id={user_id}")
    return user, None