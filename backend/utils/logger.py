# utils/logger.py

import logging
import os
from datetime import datetime

# -------------------- LOG DIRECTORY --------------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# -------------------- LOG FILE --------------------
log_filename = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y-%m-%d')}.log")

# -------------------- FORMATTER --------------------
formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# -------------------- FILE HANDLER --------------------
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# -------------------- CONSOLE HANDLER --------------------
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# -------------------- MASTER LOGGER --------------------
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger