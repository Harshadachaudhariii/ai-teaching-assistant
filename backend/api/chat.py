# api/chat.py
# EchoAI — Chat API


import asyncio
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from db.database import get_db
from services.chat_service import generate_chat_response, stream_chat_response
from core.llm_engine import register_request, cancel_request
from schemas.chat_schema import ChatRequest, ChatResponse, CancelRequest
from dependencies.auth import get_current_user
from models.user import User
from utils.logger import get_logger
from api.eval import auto_eval_and_log

logger = get_logger(__name__)
router = APIRouter()


# ─────────────────────────────────────────────
# 1. NON-STREAM
# ─────────────────────────────────────────────
@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logger.info(f"[CHAT API] Start | user_id={current_user.id} | messages={len(data.messages)}")

    if not data.messages:
        raise HTTPException(status_code=400, detail="Messages required")

    messages = [{"role": m.role, "content": m.content} for m in data.messages]

    response = generate_chat_response(db, current_user.id, messages, data.speed)

    try:
        auto_eval_and_log(
            db=db,
            user_id=current_user.id,
            question=messages[-1]["content"],
            response=response,
            mode="EchoAI",
        )
    except Exception as e:
        logger.error(f"[CHAT API] Eval failed: {e}")

    logger.info(f"[CHAT API] Success | user_id={current_user.id}")
    return {"response": response}


# ─────────────────────────────────────────────
# 2. STREAMING (SSE)
# ─────────────────────────────────────────────
@router.post("/stream")
async def chat_stream_endpoint(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not data.messages:
        raise HTTPException(status_code=400, detail="Messages required")

    request_id = getattr(data, "request_id", None) or str(uuid.uuid4())
    register_request(request_id)

    messages = [{"role": m.role, "content": m.content} for m in data.messages]
    user_id  = current_user.id
    speed    = data.speed

    logger.info(f"[CHAT STREAM] Start | user={user_id} | req={request_id}")

    async def event_generator():
        full = ""
        try:
            yield f"data: __rid__{request_id}\n\n"

            for chunk in stream_chat_response(
                    db,
                    user_id,
                    messages,
                    speed,
                    request_id
                ):
                    full += chunk
                
                    safe_chunk = chunk.replace("\n", "\\n")
                    yield f"data: {safe_chunk}\n\n"

            yield "data: [DONE]\n\n"

            try:
                auto_eval_and_log(
                    db=db,
                    user_id=user_id,
                    question=messages[-1]["content"],
                    response=full,
                    mode="EchoAI",
                )
            except Exception as e:
                logger.error(f"[STREAM EVAL ERROR] {e}")

        except asyncio.CancelledError:
            cancel_request(request_id)
            logger.info(f"[CHAT STREAM] Cancelled | req={request_id}")

        except Exception as e:
            logger.error(f"[CHAT STREAM] Error: {e} | req={request_id}")
            yield f"data: [Error: {str(e)}]\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control":     "no-cache",
            "Connection":        "keep-alive",
            "X-Accel-Buffering": "no",   
        },
    )


# ─────────────────────────────────────────────
# 3. CANCEL
# ─────────────────────────────────────────────
@router.post("/cancel")
async def cancel_chat(
    data: CancelRequest,
    current_user: User = Depends(get_current_user),
):
    found = cancel_request(data.request_id)
    logger.info(f"[CHAT CANCEL] req={data.request_id} | found={found}")
    return {
        "status":     "cancelled" if found else "not_found",
        "request_id": data.request_id,
    }