# models/otp.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from db.base import Base
from utils.logger import get_logger

logger = get_logger(__name__)

class OTPRecord(Base):
    __tablename__ = "otp_records"

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, nullable=False, index=True)
    otp_code   = Column(String, nullable=False)
    is_used    = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<OTPRecord email={self.email} used={self.is_used}>"
