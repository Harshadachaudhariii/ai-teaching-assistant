# backend/models/eval_log.py
# SQLAlchemy model for storing LLM evaluation results

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from datetime import datetime
from db.base import Base


class EvalLog(Base):
    __tablename__ = "eval_logs"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    mode         = Column(String,  nullable=False)          # "EchoAI" | "AtlasAI"
    question     = Column(String,  nullable=False)
    response     = Column(Text,    nullable=False)
    relevance    = Column(Float,   nullable=False)
    accuracy     = Column(Float,   nullable=False)
    fluency      = Column(Float,   nullable=False)
    groundedness = Column(Float,   nullable=True)           # AtlasAI only
    overall      = Column(Float,   nullable=False)
    feedback     = Column(String,  nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)