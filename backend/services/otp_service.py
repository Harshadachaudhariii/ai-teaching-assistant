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
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NexaAI Security Verification</title>
</head>

<body style="
    margin:0;
    padding:0;
    background-color:#0f1117;
    font-family:Arial, Helvetica, sans-serif;
">

<table width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>
<td align="center" style="padding:40px 20px;">

<table width="520" cellpadding="0" cellspacing="0" border="0"
style="
    background:#171a21;
    border-radius:18px;
    padding:40px;
    border:1px solid #2b2f3a;
    box-shadow:0 0 20px rgba(0,0,0,0.35);
">

<tr>
<td align="center">

<img 
    src="https://raw.githubusercontent.com/Harshadachaudhariii/ai-teaching-assistant/main/Frontend/assets/logo.png"
    width="72"
    height="72"
    style="
        border-radius:16px;
        margin-bottom:20px;
        object-fit:cover;
    "
>

<h1 style="
    color:white;
    margin:0;
    font-size:30px;
    letter-spacing:0.5px;
">
NexaAI
</h1>

<p style="
    color:#9ca3af;
    margin-top:10px;
    font-size:15px;
">
Account Security Verification
</p>

</td>
</tr>

<tr>
<td>

<p style="
    color:#d1d5db;
    margin-top:35px;
    font-size:15px;
    line-height:1.8;
">
We received a request to reset the password associated with your NexaAI account.
Use the verification code below to continue securely.
</p>

</td>
</tr>

<tr>
<td>

<div style="
    margin-top:10px;
    background:#0f1117;
    border:1px solid #2563eb;
    border-radius:14px;
    padding:30px;
    text-align:center;
">

<p style="
    color:#9ca3af;
    margin:0 0 16px 0;
    font-size:14px;
">
Verification Code
</p>

<div style="
    color:#3b82f6;
    font-size:42px;
    font-weight:bold;
    letter-spacing:10px;
">
{otp}
</div>

<p style="
    color:#6b7280;
    margin-top:18px;
    font-size:13px;
">
This code expires in {settings.OTP_EXPIRE_MINUTES} minutes
</p>

</div>

</td>
</tr>

<tr>
<td>

<div style="
    background:#111827;
    border-left:4px solid #2563eb;
    padding:18px;
    margin-top:28px;
    border-radius:10px;
">

<p style="
    margin:0;
    color:#d1d5db;
    font-size:14px;
    line-height:1.7;
">
For your security, never share this verification code with anyone.
NexaAI support will never ask for your password or verification code.
</p>

</div>

</td>
</tr>

<tr>
<td>

<div style="
    margin-top:28px;
    padding:18px;
    background:#0f172a;
    border-radius:10px;
">

<p style="
    margin:0;
    color:#9ca3af;
    font-size:14px;
    line-height:1.7;
">
If you did not initiate this request, you can safely ignore this email.
No changes will be made to your account unless the verification code is entered.
</p>

</div>

</td>
</tr>

<tr>
<td>

<hr style="
    border:none;
    border-top:1px solid #2b2f3a;
    margin:35px 0 25px 0;
">

<p style="
    color:#6b7280;
    font-size:13px;
    text-align:center;
    line-height:1.8;
    margin:0;
">
This is an automated security message from NexaAI.
Please do not reply to this email.
<br><br>
© 2026 NexaAI Technologies. All rights reserved.
</p>

</td>
</tr>

</table>

</td>
</tr>
</table>

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
            return False, "Invalid OTP"

        if record.attempts >= 3:
            record.is_used = True
            db.commit()
            return False, "Too many attempts. Request new OTP."

        # Check expiry
        if datetime.utcnow() > record.expires_at:
            # Increase attempt count before success check
            record.attempts += 1

            # Mark as used only on success
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
