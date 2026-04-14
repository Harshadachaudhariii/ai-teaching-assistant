# models/message.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base
from utils.logger import get_logger

logger = get_logger(__name__)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    role = Column(String, nullable=False)       # "user" or "assistant"
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # -------------------- RELATIONSHIP --------------------
    chat = relationship("Chat", back_populates="messages")

    def __repr__(self):
        logger.info(f"[MESSAGE MODEL] Message created: chat_id={self.chat_id} role={self.role}")
        return f"<Message id={self.id} chat_id={self.chat_id} role={self.role}>"