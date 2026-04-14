# services/rag_service.py
# atlasAI - RAG (Retrieval-Augmented Generation) Service
# services/rag_service.py
# AtlasAI Service

from core.vector_store import search_similar_chunks
from core.llm_engine import generate_atlas_response
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_rag_response(user_query: str) -> str:
    logger.info(f"[RAG SERVICE] Query received | query={user_query[:60]}")

    # Step 1: Search similar chunks
    context_df = search_similar_chunks(user_query, top_k=3)

    if context_df is None:
        logger.warning("[RAG SERVICE] No context found!")
        return "Sorry, I could not find relevant course content for your question."

    logger.info(f"[RAG SERVICE] Context retrieved | chunks={len(context_df)}")

    # Step 2: Generate response
    response = generate_atlas_response(context_df, user_query)

    logger.info(f"[RAG SERVICE] Response ready | preview={response[:60]}")
    return response