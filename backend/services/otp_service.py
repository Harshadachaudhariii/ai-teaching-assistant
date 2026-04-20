# services/otp_service.py

import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.otp import OTPRecord
from core.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- GENERATE OTP --------------------
def generate_otp() -> str:
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

# -------------------- SEND OTP EMAIL --------------------
def send_otp_email(email: str, otp: str) -> bool:
    """Send OTP via Gmail SMTP"""
    try:
        logger.info(f"[OTP SERVICE] Sending OTP email to {email}")

        # -------------------- EMAIL CONTENT --------------------
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Your NexaAI Password Reset Code"
        msg["From"]    = settings.EMAIL_FROM
        msg["To"]      = email

        # Plain text version
        text = f"""
Hi,

Your NexaAI password reset code is:

{otp}

This code expires in {settings.OTP_EXPIRE_MINUTES} minutes.

If you did not request this, please ignore this email.

— NexaAI Team
"""

        # HTML version
        html = f"""
<html>
<body style="font-family: Arial, sans-serif; background-color: #0a0a0a; color: #f3f4f6; padding: 40px;">
    <div style="max-width: 480px; margin: auto; background: #111; border: 1px solid #222; border-radius: 16px; padding: 40px;">
        <h2 style="color: #3b82f6; margin-bottom: 8px;">NexaAI</h2>
        <p style="color: #9ca3af;">Password Reset Request</p>
        <hr style="border-color: #222; margin: 24px 0;">
        <p style="font-size: 16px;">Your verification code is:</p>
        <div style="background: #1a1a1a; border: 1px solid #3b82f6; border-radius: 12px; padding: 24px; text-align: center; margin: 24px 0;">
            <h1 style="color: #3b82f6; letter-spacing: 8px; margin: 0; font-size: 36px;">{otp}</h1>
        </div>
        <p style="color: #9ca3af; font-size: 14px;">
            This code expires in <strong>{settings.OTP_EXPIRE_MINUTES} minutes</strong>.
        </p>
        <p style="color: #9ca3af; font-size: 14px;">
            If you did not request this, please ignore this email.
        </p>
        <hr style="border-color: #222; margin: 24px 0;">
        <p style="color: #4b5563; font-size: 12px; text-align: center;">— NexaAI Team</p>
    </div>
</body>
</html>
"""

        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        # -------------------- SEND VIA SMTP --------------------
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, email, msg.as_string())

        logger.info(f"[OTP SERVICE] OTP email sent successfully to {email}")
        return True

    except smtplib.SMTPAuthenticationError:
        logger.error("[OTP SERVICE] Gmail authentication failed — check EMAIL_USERNAME and EMAIL_PASSWORD in .env")
        return False

    except Exception as e:
        logger.error(f"[OTP SERVICE] Failed to send email: {str(e)}")
        return False

# -------------------- SAVE OTP TO DB --------------------
def save_otp(db: Session, email: str, otp: str) -> OTPRecord:
    """Save OTP to DB, invalidate any previous OTPs for this email"""
    try:
        # Invalidate all previous OTPs for this email
        old_otps = db.query(OTPRecord).filter(
            OTPRecord.email == email,
            OTPRecord.is_used == False
        ).all()

        for old in old_otps:
            old.is_used = True

        # Create new OTP record
        expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)

        new_otp = OTPRecord(
            email      = email,
            otp_code   = otp,
            is_used    = False,
            expires_at = expires_at
        )

        db.add(new_otp)
        db.commit()
        db.refresh(new_otp)

        logger.info(f"[OTP SERVICE] OTP saved to DB | email={email} | expires={expires_at}")
        return new_otp

    except Exception as e:
        logger.error(f"[OTP SERVICE] Failed to save OTP: {str(e)}")
        db.rollback()
        raise

# -------------------- VERIFY OTP --------------------
def verify_otp(db: Session, email: str, otp_code: str) -> tuple[bool, str]:
    """
    Verify OTP from DB
    Returns: (success: bool, message: str)
    """
    try:
        # Find latest unused OTP for this email
        record = db.query(OTPRecord).filter(
            OTPRecord.email    == email,
            OTPRecord.is_used  == False,
            OTPRecord.otp_code == otp_code
        ).order_by(OTPRecord.created_at.desc()).first()

        if not record:
            logger.warning(f"[OTP SERVICE] OTP not found | email={email}")
            return False, "Invalid OTP"

        # Check expiry
        if datetime.utcnow() > record.expires_at:
            record.is_used = True
            db.commit()
            logger.warning(f"[OTP SERVICE] OTP expired | email={email}")
            return False, "OTP has expired. Please request a new one."

        # Mark as used
        record.is_used = True
        db.commit()

        logger.info(f"[OTP SERVICE] OTP verified successfully | email={email}")
        return True, "OTP verified"

    except Exception as e:
        logger.error(f"[OTP SERVICE] Verification error: {str(e)}")
        return False, "Verification failed"

# -------------------- FULL FLOW: GENERATE + SAVE + SEND --------------------
def create_and_send_otp(db: Session, email: str) -> tuple[bool, str]:
    """
    Main function called by the API endpoint.
    Generates OTP → Saves to DB → Sends email
    Returns: (success: bool, message: str)
    """
    try:
        otp = generate_otp()
        save_otp(db, email, otp)
        sent = send_otp_email(email, otp)

        if sent:
            logger.info(f"[OTP SERVICE] OTP created and sent | email={email}")
            return True, "OTP sent to your email"
        else:
            return False, "Failed to send OTP email. Check email configuration."

    except Exception as e:
        logger.error(f"[OTP SERVICE] create_and_send_otp error: {str(e)}")
        return False, str(e)
