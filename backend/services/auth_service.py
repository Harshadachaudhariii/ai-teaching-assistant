# services/auth_service.py

from sqlalchemy.orm import Session
from models.user import User
from core.security import hash_password, verify_password, create_access_token
from utils.logger import get_logger

logger = get_logger(__name__)

def register_user(db: Session, name: str, email: str, password: str):
    logger.info(f"[AUTH SERVICE] Register attempt | email={email}")

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        logger.warning(f"[AUTH SERVICE] User already exists | email={email}")
        return None, "User already exists"

    # Create new user
    new_user = User(
        name=name,
        email=email,
        password_hash=hash_password(password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"[AUTH SERVICE] User registered successfully | email={email}")
    return new_user, None


def login_user(db: Session, email: str, password: str):
    logger.info(f"[AUTH SERVICE] Login attempt | email={email}")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"[AUTH SERVICE] User not found | email={email}")
        return None, "User not found"

    if not verify_password(password, user.password_hash):
        logger.warning(f"[AUTH SERVICE] Incorrect password | email={email}")
        return None, "Incorrect password"

    # Create JWT token
    token = create_access_token({"user_id": user.id})

    logger.info(f"[AUTH SERVICE] Login successful | email={email}")
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}, None