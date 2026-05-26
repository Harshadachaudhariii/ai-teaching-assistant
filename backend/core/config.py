# core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.logger import get_logger
import os 
logger = get_logger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = f"sqlite:///{os.path.join(BASE_DIR, 'db', 'nexa_ai.db')}"
# -------------------- SETTINGS --------------------
class Settings(BaseSettings):

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_DB_PATH)

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    #  Email OTP Settings
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    EMAIL_FROM: str = ""

    # OTP expiry in minutes
    OTP_EXPIRE_MINUTES: int = 5

    # Modern Pydantic V2 Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

# -------------------- INSTANCE --------------------
settings = Settings()

logger.info(f"[CONFIG] Database: {settings.DATABASE_URL}")
logger.info(f"[CONFIG] Ollama: {settings.OLLAMA_BASE_URL}")
logger.info(f"[CONFIG] Email: {settings.EMAIL_USERNAME}")
logger.info("[CONFIG] Settings loaded successfully")
