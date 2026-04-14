# models/user.py
# models/user.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base
from utils.logger import get_logger

logger = get_logger(__name__)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # -------------------- RELATIONSHIPS --------------------
    chats = relationship("Chat", back_populates="user")  # ← added

    def __repr__(self):
        logger.info(f"[USER MODEL] User object created: {self.email}")
        return f"<User id={self.id} email={self.email}>"