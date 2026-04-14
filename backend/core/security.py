# core/security.py

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from utils.logger import get_logger
import os
from core.config import settings

logger = get_logger(__name__)

# -------------------- CONFIG --------------------
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# -------------------- PASSWORD HASHING --------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    logger.info("[SECURITY] Hashing password")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    logger.info("[SECURITY] Verifying password")
    return pwd_context.verify(plain_password, hashed_password)

# -------------------- JWT TOKEN --------------------
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # ✅ fixed
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"[SECURITY] Access token created for: {data}")
    return token

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info("[SECURITY] Token decoded successfully")
        return payload
    except Exception as e:
        logger.error(f"[SECURITY] Token decode failed: {str(e)}")
        return None