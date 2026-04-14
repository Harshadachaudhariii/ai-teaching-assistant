# db/base.py

from sqlalchemy.orm import declarative_base
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- BASE --------------------
Base = declarative_base()

logger.info("SQLAlchemy Base initialized")