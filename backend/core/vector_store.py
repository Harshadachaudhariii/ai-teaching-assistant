# # core/vector_store.py

# import numpy as np
# import requests
# from sklearn.metrics.pairwise import cosine_similarity
# from core.embeddings_loader import embeddings_df
# from utils.logger import get_logger
# from core.config import settings

# logger = get_logger(__name__)

# # -------------------- CREATE EMBEDDING --------------------
# def create_embedding(text_list: list) -> list:
#     try:
#         logger.info(f"[VECTOR STORE] Creating embedding for: {text_list[0][:60]}")

#         r = requests.post(f"{settings.OLLAMA_BASE_URL}/api/embed", json={
#             "model": "bge-m3",
#             "input": text_list
#         })

#         embeddings = r.json()["embeddings"]
#         logger.info("[VECTOR STORE] Embedding created successfully")
#         return embeddings

#     except Exception as e:
#         logger.error(f"[VECTOR STORE] Embedding error: {str(e)}")
#         return []

# # -------------------- SIMILARITY SEARCH --------------------
# def search_similar_chunks(query: str, top_k: int = 3):
#     try:
#         if embeddings_df is None:
#             logger.warning("[VECTOR STORE] Embeddings not loaded!")
#             return None

#         # Step 1: Embed the query
#         question_embedding = create_embedding([query])[0]

#         # Step 2: Cosine similarity
#         similarities = cosine_similarity(
#             np.vstack(embeddings_df['embedding']),
#             [question_embedding]
#         ).flatten()

#         # Step 3: Top K results
#         top_indices = similarities.argsort()[::-1][:top_k]
#         result_df = embeddings_df.loc[top_indices]

#         logger.info(f"[VECTOR STORE] Top {top_k} chunks retrieved")
#         return result_df

#     except Exception as e:
#         logger.error(f"[VECTOR STORE] Search error: {str(e)}")
#         return None

# core/vector_store.py

import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity
from core.embeddings_loader import embeddings_df
from utils.logger import get_logger
from core.config import settings

logger = get_logger(__name__)

# -------------------- SIMILARITY THRESHOLD --------------------
# ✅ Only return chunks with similarity > threshold (avoids hallucination)
SIMILARITY_THRESHOLD = 0.55
TOP_K = 5

# -------------------- CREATE EMBEDDING --------------------
def create_embedding(text_list: list) -> list:
    try:
        logger.info(f"[VECTOR STORE] Creating embedding | query={text_list[0][:60]}")

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

# -------------------- FORMAT TIMESTAMP --------------------
def format_time(seconds: float) -> str:
    """Convert seconds to MM:SS format"""
    try:
        total   = int(float(seconds))
        minutes = total // 60
        secs    = total % 60
        return f"{minutes:02d}:{secs:02d}"
    except:
        return "00:00"

# -------------------- SIMILARITY SEARCH --------------------
def search_similar_chunks(query: str, top_k: int = TOP_K):
    try:
        if embeddings_df is None:
            logger.warning("[VECTOR STORE] Embeddings not loaded!")
            return None

        # Step 1: Embed the query
        question_embedding = create_embedding([query])[0]

        # Step 2: Cosine similarity
        embeddings_matrix = np.vstack(embeddings_df['embedding'].values)
        similarities = cosine_similarity(
            embeddings_matrix,
            [question_embedding]
        ).flatten()

        # Step 3: ✅ Filter by threshold — avoid low quality matches
        filtered_idx = [
            i for i, score in enumerate(similarities)
            if score > SIMILARITY_THRESHOLD
        ]

        if not filtered_idx:
            logger.warning(f"[VECTOR STORE] No chunks above threshold {SIMILARITY_THRESHOLD} | query={query[:60]}")
            return None

        # Step 4: Top-K from filtered results
        top_indices = sorted(
            filtered_idx,
            key=lambda i: similarities[i],
            reverse=True
        )[:top_k]

        result_df = embeddings_df.loc[top_indices].copy()

        # Step 5: ✅ Convert timestamps to MM:SS format
        result_df["start"] = result_df["start"].apply(format_time)
        result_df["end"]   = result_df["end"].apply(format_time)

        # Log top scores for debugging
        for i in top_indices:
            logger.info(
                f"[VECTOR STORE] Match | score={similarities[i]:.4f} | "
                f"video={embeddings_df.iloc[i]['number']} | "
                f"title={embeddings_df.iloc[i]['title'][:40]}"
            )

        logger.info(f"[VECTOR STORE] Retrieved {len(result_df)} chunks above threshold")
        return result_df

    except Exception as e:
        logger.error(f"[VECTOR STORE] Search error: {str(e)}")
        return None
