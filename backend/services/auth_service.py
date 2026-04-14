# services/auth_service.py

from sqlalchemy.orm import Session
from models.user import User
from core.security import hash_password, verify_password, create_access_token


def register_user(db: Session, name: str, email: str, password: str):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
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

    return new_user, None


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None, "User not found"

    if not verify_password(password, user.password_hash):
        return None, "Incorrect password"

    # Create JWT token
    token = create_access_token({"user_id": user.id})

    return {"access_token": token, "user_id": user.id}, None