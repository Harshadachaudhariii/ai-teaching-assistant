#  db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.logger import get_logger
import os
from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)

# -------------------- DATABASE URL --------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nexa_ai.db")

logger.info(f"Connecting to database: {DATABASE_URL}")

# -------------------- ENGINE --------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite only
)

logger.info("Database engine created successfully")

# -------------------- SESSION --------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

logger.info("SessionLocal configured")

# -------------------- DEPENDENCY --------------------
def get_db():
    db = SessionLocal()
    try:
        logger.info("Database session opened")
        yield db
    finally:
        db.close()
        logger.info("Database session closed")