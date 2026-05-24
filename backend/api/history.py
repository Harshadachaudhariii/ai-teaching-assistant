# api/history.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from pydantic import BaseModel
from datetime import datetime

from db.database import get_db
from dependencies.auth import get_current_user
from models.user import User
from models.chat import Chat
from models.message import Message
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

# ============================================================
# SCHEMAS
# ============================================================
class MessageOut(BaseModel):
    role: str
    content: str
    timestamp: datetime | None = None
    class Config:
        from_attributes = True

class ChatOut(BaseModel):
    id: int
    client_id: str | None = None   # frontend uuid
    title: str
    mode: str
    created_at: datetime
    messages: List[MessageOut]
    class Config:
        from_attributes = True

class SaveChatRequest(BaseModel):
    client_id: str          # frontend uuid — so we can sync
    title: str
    mode: str               # "EchoAI" | "AtlasAI"
    messages: List[dict]    # [{role, content}]

class UpdateTitleRequest(BaseModel):
    title: str

# ============================================================
# 1. GET ALL CHATS (sidebar history on login)
# ============================================================
@router.get("/")
def get_all_chats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chats = (
        db.query(Chat)
        .filter(Chat.user_id == current_user.id)
        .order_by(desc(Chat.created_at))
        .all()
    )

    result = []
    for chat in chats:
        messages = (
            db.query(Message)
            .filter(Message.chat_id == chat.id)
            .order_by(Message.timestamp)
            .all()
        )
        result.append({
            "id":         chat.id,
            "client_id":  chat.client_id,
            "title":      chat.title,
            "mode":       chat.assistant_name,
            "created_at": str(chat.created_at),
            "messages":   [{"role": m.role, "content": m.content} for m in messages],
        })

    logger.info(f"[HISTORY] Loaded {len(result)} chats | user_id={current_user.id}")
    return result

# ============================================================
# 2. SAVE / UPDATE CHAT (called after each message)
# ============================================================
@router.post("/save")
def save_chat(
    data: SaveChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if chat with this client_id already exists
    existing = db.query(Chat).filter(
        Chat.client_id == data.client_id,
        Chat.user_id   == current_user.id,
    ).first()

    if existing:
        # Update title + replace all messages
        existing.title = data.title
        db.query(Message).filter(Message.chat_id == existing.id).delete()
        for msg in data.messages:
            db.add(Message(
                chat_id = existing.id,
                user_id = current_user.id if msg["role"] == "user" else None,
                role    = msg["role"],
                content = msg["content"],
            ))
        db.commit()
        logger.info(f"[HISTORY] Updated chat | chat_id={existing.id}")
        return {"chat_id": existing.id, "status": "updated"}
    else:
        # Create new chat
        new_chat = Chat(
            user_id        = current_user.id,
            client_id      = data.client_id,
            title          = data.title,
            assistant_name = data.mode,
        )
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)

        for msg in data.messages:
            db.add(Message(
                chat_id = new_chat.id,
                user_id = current_user.id if msg["role"] == "user" else None,
                role    = msg["role"],
                content = msg["content"],
            ))
        db.commit()
        logger.info(f"[HISTORY] Saved new chat | chat_id={new_chat.id}")
        return {"chat_id": new_chat.id, "status": "created"}

# ============================================================
# 3. UPDATE TITLE ONLY (rename dialog)
# ============================================================
@router.patch("/{client_id}/title")
def update_title(
    client_id: str,
    data: UpdateTitleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = db.query(Chat).filter(
        Chat.client_id == client_id,
        Chat.user_id   == current_user.id,
    ).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat.title = data.title
    db.commit()
    logger.info(f"[HISTORY] Title updated | client_id={client_id} | title={data.title}")
    return {"status": "ok"}

# ============================================================
# 4. DELETE CHAT
# ============================================================
@router.delete("/{client_id}")
def delete_chat(
    client_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = db.query(Chat).filter(
        Chat.client_id == client_id,
        Chat.user_id   == current_user.id,
    ).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    db.query(Message).filter(Message.chat_id == chat.id).delete()
    db.delete(chat)
    db.commit()
    logger.info(f"[HISTORY] Deleted chat | client_id={client_id}")
    return {"status": "deleted"}