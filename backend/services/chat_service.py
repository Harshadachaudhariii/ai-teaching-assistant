# services/chat_service.py
# EchoAI Service
from sqlalchemy.orm import Session
from typing import Generator, Optional

from models.chat import Chat
from models.message import Message
from models.user import User

from core.llm_engine import generate_echo_response, generate_echo_stream
from utils.logger import get_logger
from fastapi import HTTPException

logger = get_logger(__name__)


def generate_chat_response(
    db: Session,
    user_id: int,
    messages: list,
    speed: str = "default"
) -> str:
    """
    Non-streaming response (main chat).
    Saves chat + messages to DB.
    """
    logger.info(f"[CHAT SERVICE] Processing request for User ID: {user_id}")
    logger.info(f"[CHAT SERVICE] LLM Request | Speed: {speed} | messages={len(messages)}")

    #  Validate user (from Claude version)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    #  Generate response
    response = generate_echo_response(messages, speed)
    logger.info(f"[CHAT SERVICE] Response ready | preview={response[:60]}")

    try:
        #  Create Chat
        new_chat = Chat(user_id=user_id)
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)

        logger.info(f"[CHAT SERVICE] DB | Chat ID {new_chat.id} created")

        #  Save messages
        user_query = messages[-1]["content"]

        db_user_msg = Message(
            chat_id=new_chat.id,
            user_id=user_id,
            role="user",
            content=user_query
        )

        db_ai_msg = Message(
            chat_id=new_chat.id,
            user_id=None,
            role="assistant",
            content=response
        )

        db.add_all([db_user_msg, db_ai_msg])
        db.commit()

        logger.info("[CHAT SERVICE] DB | Messages saved successfully")

    except Exception as e:
        db.rollback()
        logger.error(f"[CHAT SERVICE] DATABASE ERROR: {str(e)}")

    return response
def save_chat_after_stream(db, user_id, messages, full_response):
    new_chat = Chat(user_id=user_id)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    user_query = messages[-1]["content"]

    db.add_all([
        Message(
            chat_id=new_chat.id,
            user_id=user_id,
            role="user",
            content=user_query
        ),
        Message(
            chat_id=new_chat.id,
            user_id=None,
            role="assistant",
            content=full_response
        )
    ])

    db.commit()

def stream_chat_response(
    db: Session,
    user_id: int,
    messages: list,
    speed: str = "default",
    request_id: Optional[str] = None
) -> Generator[str, None, None]:

    logger.info(f"[CHAT SERVICE] Streaming started | user_id={user_id}")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    full_response = ""

    try:
        for chunk in generate_echo_stream(messages, speed, request_id):
            full_response += chunk
            yield chunk

        logger.info("[CHAT SERVICE] Streaming completed")

        # IMPORTANT: DB save happens AFTER streaming
        save_chat_after_stream(db, user_id, messages, full_response)

        logger.info("[CHAT SERVICE] DB saved after streaming")

    except Exception as e:
        db.rollback()
        logger.error(f"[CHAT SERVICE] STREAM ERROR: {str(e)}")