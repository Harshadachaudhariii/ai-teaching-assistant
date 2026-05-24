# api/rag.py
# AtlasAI — RAG based

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.background import BackgroundTasks
import threading
from services.rag_service import generate_rag_stream
from schemas.chat_schema import RAGRequest, ChatResponse
from dependencies.auth import get_current_user
from models.user import User
from utils.logger import get_logger
from db.database import get_db
from sqlalchemy.orm import Session
import uuid
from pydantic import BaseModel
from core.llm_engine import cancel_request
from api.eval import auto_eval_and_log
logger = get_logger(__name__)

router = APIRouter()

# -------------------- RAG ENDPOINT --------------------
@router.post("/")
async def rag_endpoint(
    data: RAGRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    logger.info(
        f"[RAG API] Stream request | "
        f"user_id={current_user.id} | "
        f"query={data.query[:60]}"
    )

    if not data.query:
        raise HTTPException(status_code=400, detail="Query is required")

    full_response = []

    request_id = str(uuid.uuid4())

    original_stream = generate_rag_stream(
        data.query,
        request_id=request_id,
    )

    # ─────────────────────────────
    # capture stream for evaluation
    # ─────────────────────────────
    def wrapped_stream():

        for chunk in original_stream:

            try:

                if chunk.startswith("data: "):

                    token = chunk.replace("data: ", "")

                    if token != "[DONE]":
                        full_response.append(token)

            except Exception:
                pass

            yield chunk

    # ─────────────────────────────
    # background evaluation
    # ─────────────────────────────
    def run_background_eval():

        try:

            response_text = "".join(full_response).strip()

            if not response_text:
                return

            auto_eval_and_log(
                db=db,
                user_id=current_user.id,
                question=data.query,
                response=response_text,
                mode="AtlasAI",
            )

        except Exception as e:

            logger.error(f"[RAG API] Background eval failed: {e}")

    background_tasks.add_task(run_background_eval)

    response = StreamingResponse(
        wrapped_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "X-Request-ID": request_id,
        }
    )

    return response


class CancelRequest(BaseModel):
    request_id: str


@router.post("/cancel")
async def cancel_rag_stream(
    data: CancelRequest,
    current_user: User = Depends(get_current_user),
):

    cancelled = cancel_request(data.request_id)

    if cancelled:

        logger.info(
            f"[RAG API] Cancel success | "
            f"user_id={current_user.id} | "
            f"req={data.request_id}"
        )

        return {"success": True}

    return {"success": False}