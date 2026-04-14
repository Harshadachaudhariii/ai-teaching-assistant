# core/config.py

from pydantic_settings import BaseSettings
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- SETTINGS --------------------
class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# -------------------- INSTANCE --------------------
settings = Settings()

logger.info(f"[CONFIG] Database: {settings.DATABASE_URL}")
logger.info(f"[CONFIG] Ollama: {settings.OLLAMA_BASE_URL}")
logger.info("[CONFIG] Settings loaded successfully")