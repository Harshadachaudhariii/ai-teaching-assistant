# schemas/user_schema.py

from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- USER RESPONSE --------------------
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    # Modern Pydantic V2 Configuration
    model_config = ConfigDict(from_attributes=True)

# -------------------- USER UPDATE --------------------
class UserUpdateRequest(BaseModel):
    name: str | None = None
    email: EmailStr | None = None