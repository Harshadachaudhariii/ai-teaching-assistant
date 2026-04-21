# api/chat.py
# EchoAI — General LLM

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from db.database import get_db
from services.chat_service import generate_chat_response
from schemas.chat_schema import ChatRequest, ChatResponse
from dependencies.auth import get_current_user
from models.user import User
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

# -------------------- CHAT db --------------------
@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)  # Database session injected
):
    logger.info(f"[CHAT API] Start | User: {current_user.email} | Messages: {len(data.messages)}")

    if not data.messages:
        logger.warning("[CHAT API] Failure | No messages provided")
        raise HTTPException(status_code=400, detail="Messages required")

    # Convert schema to list of dicts
    messages = [{"role": m.role, "content": m.content} for m in data.messages]

    # ✅ Pass db and user_id to service
    logger.info(f"[CHAT API] Handover to Service | user_id={current_user.id}")
    response = generate_chat_response(db, current_user.id, messages, data.speed)

    logger.info(f"[CHAT API] Success | user_id={current_user.id} | Sent AI response")
    return {"response": response}


# -------------------- CHAT ENDPOINT --------------------
@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    data: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    EchoAI — General purpose LLM
    speed = "default" → llama3:latest
    speed = "fast"    → phi3:mini
    """
    logger.info(f"[CHAT API] Request | user_id={current_user.id} | speed={data.speed} | messages={len(data.messages)}")

    if not data.messages:
        logger.warning("[CHAT API] Empty messages received")
        raise HTTPException(status_code=400, detail="Messages required")

    # Convert schema to dict for service
    messages = [{"role": m.role, "content": m.content} for m in data.messages]

    response = generate_chat_response(messages, data.speed)

    logger.info(f"[CHAT API] Response ready | user_id={current_user.id} | preview={response[:60]}")
    return {"response": response}