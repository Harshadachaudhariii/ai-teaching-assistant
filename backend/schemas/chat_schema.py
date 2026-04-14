# schemas/chat_schema.py

from pydantic import BaseModel
from datetime import datetime
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- MESSAGE --------------------
class MessageSchema(BaseModel):
    role: str        # "user" or "assistant"
    content: str
    timestamp: datetime | None = None

    class Config:
        from_attributes = True

# -------------------- CHAT REQUEST --------------------
class ChatRequest(BaseModel):
    messages: List[MessageSchema]
    speed: str = "default"   # "default" = llama3 | "fast" = phi3:mini

# -------------------- RAG REQUEST --------------------
class RAGRequest(BaseModel):
    query: str

# -------------------- CHAT RESPONSE --------------------
class ChatResponse(BaseModel):
    response: str

# -------------------- CHAT HISTORY --------------------
class ChatHistoryResponse(BaseModel):
    chat_id: int
    messages: List[MessageSchema]