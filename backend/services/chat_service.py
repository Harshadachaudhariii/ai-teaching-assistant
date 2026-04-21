# services/chat_service.py
# EchoAI Service
from sqlalchemy.orm import Session
from models.chat import Chat
from models.message import Message
from core.llm_engine import generate_echo_response
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_chat_response(db: Session, user_id: int, messages: list, speed: str = "default") -> str:
    """
    speed = "default" → llama3:latest  (balanced)
    speed = "fast"    → phi3:mini      (quick)
    speed = "smart"   → llama3         (deep — same as default but higher tokens)
    """
    logger.info(f"[CHAT SERVICE] Processing request for User ID: {user_id}")
    logger.info(f"[CHAT SERVICE] LLM Request | Speed: {speed} | messages={len(messages)}")
    
    # 1. Call LLM
    response = generate_echo_response(messages, speed)
    logger.info(f"[CHAT SERVICE] Response ready | preview={response[:60]}")
    logger.info("[CHAT SERVICE] LLM Response Generated")
    
    try:
        # 2. Create Chat Record
        logger.info(f"[CHAT SERVICE] DB | Creating Chat for user_id={user_id}")
        new_chat = Chat(user_id=user_id)
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        logger.info(f"[CHAT SERVICE] DB | Chat ID {new_chat.id} created successfully")
        
        # 3. Create Message Records
        user_query = messages[-1]["content"]
        logger.info(f"[CHAT SERVICE] DB | Preparing user & assistant messages for Chat ID {new_chat.id}")
        db_user_msg = Message(chat_id=new_chat.id, user_id=user_id,role="user", content=user_query)
        db_ai_msg = Message(chat_id=new_chat.id, user_id=None,role="assistant", content=response)
        db.add(db_user_msg)
        db.add(db_ai_msg)
        
        # 4. Final Commit
        db.commit()
        logger.info(f"[CHAT SERVICE] DB | Messages committed successfully to SQLite")
    except Exception as e:
        db.rollback()
        logger.error(f"[CHAT SERVICE] DATABASE ERROR | Could not save chat: {str(e)}")
        # We still return the response so the user gets an answer even if DB fails
    return response
