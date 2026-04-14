# core/embeddings_loader.py

import joblib
import os
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- PATH --------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "LLM", "embeddings.joblib")

logger.info(f"[EMBEDDINGS] Looking for embeddings at: {EMBEDDINGS_PATH}")
# -------------------- LOAD ONCE AT STARTUP --------------------
def load_embeddings():
    try:
        if not os.path.exists(EMBEDDINGS_PATH):
            logger.warning(f"[EMBEDDINGS] File not found at {EMBEDDINGS_PATH}")
            return None

        df = joblib.load(EMBEDDINGS_PATH)
        logger.info(f"[EMBEDDINGS] Loaded successfully | rows={len(df)}")
        return df

    except Exception as e:
        logger.error(f"[EMBEDDINGS] Failed to load: {str(e)}")
        return None

# -------------------- GLOBAL INSTANCE --------------------
embeddings_df = load_embeddings()
