# core/vector_store.py

import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity
from core.embeddings_loader import embeddings_df
from utils.logger import get_logger
from core.config import settings

logger = get_logger(__name__)

# -------------------- CREATE EMBEDDING --------------------
def create_embedding(text_list: list) -> list:
    try:
        logger.info(f"[VECTOR STORE] Creating embedding for: {text_list[0][:60]}")

        r = requests.post(f"{settings.OLLAMA_BASE_URL}/api/embed", json={
            "model": "bge-m3",
            "input": text_list
        })

        embeddings = r.json()["embeddings"]
        logger.info("[VECTOR STORE] Embedding created successfully")
        return embeddings

    except Exception as e:
        logger.error(f"[VECTOR STORE] Embedding error: {str(e)}")
        return []

# -------------------- SIMILARITY SEARCH --------------------
def search_similar_chunks(query: str, top_k: int = 3):
    try:
        if embeddings_df is None:
            logger.warning("[VECTOR STORE] Embeddings not loaded!")
            return None

        # Step 1: Embed the query
        question_embedding = create_embedding([query])[0]

        # Step 2: Cosine similarity
        similarities = cosine_similarity(
            np.vstack(embeddings_df['embedding']),
            [question_embedding]
        ).flatten()

        # Step 3: Top K results
        top_indices = similarities.argsort()[::-1][:top_k]
        result_df = embeddings_df.loc[top_indices]

        logger.info(f"[VECTOR STORE] Top {top_k} chunks retrieved")
        return result_df

    except Exception as e:
        logger.error(f"[VECTOR STORE] Search error: {str(e)}")
        return None