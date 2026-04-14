# schemas/auth_schema.py

from pydantic import BaseModel, EmailStr
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- REGISTER --------------------
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

# -------------------- LOGIN --------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# -------------------- TOKEN RESPONSE --------------------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int