# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import engine
from db.base import Base

# ── Models (must import before create_all) ───────────────────
from models.user import User
from models.chat import Chat
from models.message import Message
from models.otp import OTPRecord

# ── Routers ──────────────────────────────────────────────────
from api.auth import router as auth_router
from api.user import router as user_router
from api.chat import router as chat_router
from api.rag import router as rag_router
from api.history import router as history_router
from models.eval_log import EvalLog
from utils.logger import get_logger
from api.eval import router as eval_router

logger = get_logger(__name__)

# ── Create tables ─────────────────────────────────────────────
Base.metadata.create_all(bind=engine)
logger.info("[MAIN] Database tables created")

# ── Lifespan Handler ──────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This block executes BEFORE the server starts up (Startup)
    logger.info("[MAIN] Server started successfully")
    logger.info("[MAIN] EchoAI  → /chat")
    logger.info("[MAIN] AtlasAI → /rag")
    logger.info("[MAIN] Auth    → /auth")
    logger.info("[MAIN] User    → /user")
    logger.info("[MAIN] Docs    → /docs")
    
    yield  # The app runs and handles requests here
    
    # This block executes AFTER the server receives a shutdown signal (Shutdown)
    logger.info("[MAIN] Server shutting down...")
    
# ── App ───────────────────────────────────────────────────────
app = FastAPI(
    title="NexaAI Teaching Assistant Backend",
    description="EchoAI + AtlasAI Backend",
    version="1.0.0",
    lifespan=lifespan  # Registered the lifespan handler here
)

app.include_router(eval_router, prefix="/eval", tags=["Eval"])

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("[MAIN] CORS middleware added")

# ── Routes ────────────────────────────────────────────────────
app.include_router(auth_router,    prefix="/auth",    tags=["Auth"])
app.include_router(user_router,    prefix="/user",    tags=["User"])
app.include_router(chat_router,    prefix="/chat",    tags=["EchoAI"])
app.include_router(rag_router,     prefix="/rag",     tags=["AtlasAI"])
app.include_router(history_router, prefix="/history", tags=["History"])
logger.info("[MAIN] All routers registered")

# 1. Define the Lifespan (This replaces @app.on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Everything here runs on STARTUP
    logger.info("[MAIN] Server started successfully")
    logger.info("[MAIN] EchoAI  → /chat")
    logger.info("[MAIN] AtlasAI → /rag")
    logger.info("[MAIN] Auth    → /auth")
    logger.info("[MAIN] User    → /user")
    logger.info("[MAIN] Docs    → /docs")
    
    yield  # This acts as the separator. The app runs here.
    
    # Everything here runs on SHUTDOWN
    logger.info("[MAIN] Server shutting down...")
@app.get("/")
def root():
    logger.info("[MAIN] Root endpoint hit")
    return {
        "message": "AI Teaching Assistant Backend is running",
        "docs":    "/docs",
        "version": "1.0.0",
    }

