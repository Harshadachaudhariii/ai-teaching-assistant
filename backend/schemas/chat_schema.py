# schemas/chat_schema.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- MESSAGE --------------------
class MessageSchema(BaseModel):
    role: str        # "user" or "assistant"
    content: str
    timestamp: datetime | None = None

    # Modern Pydantic V2 Configuration
    model_config = ConfigDict(from_attributes=True)

# -------------------- CHAT REQUEST --------------------
class ChatRequest(BaseModel):
    messages: List[MessageSchema]
    speed: str = "default"   # "default" = llama3 | "fast" = phi3:mini
    request_id: Optional[str] = None 

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
    
# --------------------Cancel Request--------------------
class CancelRequest(BaseModel):
    request_id: str