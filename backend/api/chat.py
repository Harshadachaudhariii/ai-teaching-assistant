# api/chat.py
# EchoAI — General LLM

from fastapi import APIRouter, Depends, HTTPException
from services.chat_service import generate_chat_response
from schemas.chat_schema import ChatRequest, ChatResponse
from dependencies.auth import get_current_user
from models.user import User
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

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