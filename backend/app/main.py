# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import engine
from db.base import Base

# -------------------- MODELS (must import before create_all) --------------------
from models.user import User
from models.chat import Chat
from models.message import Message
from models.otp import OTPRecord        # ✅ OTP table

# -------------------- ROUTERS --------------------
from api.auth import router as auth_router
from api.user import router as user_router
from api.chat import router as chat_router
from api.rag import router as rag_router

from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- CREATE TABLES --------------------
Base.metadata.create_all(bind=engine)
logger.info("[MAIN] Database tables created")

# -------------------- APP --------------------
app = FastAPI(
    title="AI Teaching Assistant",
    description="EchoAI + AtlasAI Backend",
    version="1.0.0"
)

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("[MAIN] CORS middleware added")

# -------------------- ROUTES --------------------
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(chat_router, prefix="/chat", tags=["EchoAI"])
app.include_router(rag_router,  prefix="/rag",  tags=["AtlasAI"])

logger.info("[MAIN] All routers registered")

# -------------------- ROOT --------------------
@app.get("/")
def root():
    logger.info("[MAIN] Root endpoint hit")
    return {
        "message": "AI Teaching Assistant Backend is running",
        "docs":    "/docs",
        "version": "1.0.0"
    }

# -------------------- STARTUP --------------------
@app.on_event("startup")
async def startup_event():
    logger.info("[MAIN] 🚀 Server started successfully")
    logger.info("[MAIN] EchoAI  → /chat")
    logger.info("[MAIN] AtlasAI → /rag")
    logger.info("[MAIN] Auth    → /auth")
    logger.info("[MAIN] User    → /user")
    logger.info("[MAIN] Docs    → /docs")

# -------------------- SHUTDOWN --------------------
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("[MAIN] Server shutting down...")
