# api/auth.py

# api/auth.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from db.database import get_db
from services.auth_service import register_user, login_user
from services.otp_service import create_and_send_otp, verify_otp
from core.security import hash_password
from schemas.auth_schema import RegisterRequest, LoginRequest
from dependencies.auth import get_current_user
from models.user import User
from utils.logger import get_logger

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
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"[AUTH API] Login request | email={data.email}")

    result, error = login_user(db, data.email, data.password)

    if error:
        logger.warning(f"[AUTH API] Login failed | {error}")
        raise HTTPException(status_code=401, detail=error)

    logger.info(f"[AUTH API] Login success | user_id={result['user_id']}")
    return result

# -------------------- LOGIN FORM (Swagger Authorize button) --------------------
@router.post("/login-form")
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"[AUTH API] Login form request | email={form_data.username}")

    result, error = login_user(db, form_data.username, form_data.password)

    if error:
        logger.warning(f"[AUTH API] Login form failed | {error}")
        raise HTTPException(status_code=401, detail=error)

    logger.info(f"[AUTH API] Login form success")
    return result

# -------------------- ME --------------------
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    logger.info(f"[AUTH API] Me request | user_id={current_user.id}")
    return {
        "user_id":    current_user.id,
        "name":       current_user.name,
        "email":      current_user.email,
        "created_at": current_user.created_at
    }

# ==========================================
# OTP ENDPOINTS
# ==========================================

# -------------------- FORGOT PASSWORD --------------------
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    logger.info(f"[AUTH API] Forgot password request | email={data.email}")

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        logger.warning(f"[AUTH API] User not found | email={data.email}")
        raise HTTPException(status_code=404, detail="No account found with this email")

    success, message = create_and_send_otp(db, data.email)

    if not success:
        logger.error(f"[AUTH API] OTP send failed | reason={message}")
        raise HTTPException(status_code=500, detail=message)

    logger.info(f"[AUTH API] OTP sent | email={data.email}")
    return {"message": f"OTP sent to {data.email}"}

# -------------------- VERIFY OTP --------------------
class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

@router.post("/verify-otp")
def verify_otp_endpoint(data: VerifyOTPRequest, db: Session = Depends(get_db)):
    logger.info(f"[AUTH API] Verify OTP | email={data.email}")

    success, message = verify_otp(db, data.email, data.otp)

    if not success:
        logger.warning(f"[AUTH API] OTP failed | reason={message}")
        raise HTTPException(status_code=400, detail=message)

    logger.info(f"[AUTH API] OTP verified | email={data.email}")
    return {"message": "OTP verified successfully"}

# -------------------- RESET PASSWORD --------------------
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    logger.info(f"[AUTH API] Reset password | email={data.email}")

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if len(data.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    user.password_hash = hash_password(data.new_password)
    db.commit()

    logger.info(f"[AUTH API] Password reset success | email={data.email}")
    return {"message": "Password updated successfully"}