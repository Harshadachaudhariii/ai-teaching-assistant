# models/chat.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base
from utils.logger import get_logger

logger = get_logger(__name__)

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assistant_name = Column(String, nullable=False) # "echoai" or "atlasai"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
    # -------------------- RELATIONSHIPS --------------------
    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat")

    def __repr__(self):
        logger.info(f"[CHAT MODEL] Chat object created: id={self.id} user_id={self.user_id}")
        return f"<Chat id={self.id} user_id={self.user_id}>"