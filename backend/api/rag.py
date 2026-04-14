# api/rag.py
# AtlasAI — RAG based

from fastapi import APIRouter, Depends, HTTPException
from services.rag_service import generate_rag_response
from schemas.chat_schema import RAGRequest, ChatResponse
from dependencies.auth import get_current_user
from models.user import User
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

# -------------------- RAG ENDPOINT --------------------
@router.post("/", response_model=ChatResponse)
async def rag_endpoint(
    data: RAGRequest,
    current_user: User = Depends(get_current_user)
):
    """
    AtlasAI — RAG based
    Only answers course related questions
    """
    logger.info(f"[RAG API] Request | user_id={current_user.id} | query={data.query[:60]}")

    if not data.query:
        logger.warning("[RAG API] Empty query received")
        raise HTTPException(status_code=400, detail="Query is required")

    response = generate_rag_response(data.query)

    logger.info(f"[RAG API] Response ready | user_id={current_user.id} | preview={response[:60]}")
    return {"response": response}