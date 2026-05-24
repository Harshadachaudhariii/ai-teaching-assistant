# services/rag_service.py
# atlasAI - RAG (Retrieval-Augmented Generation) Service
# AtlasAI Service

from core.vector_store import search_similar_chunks
from core.llm_engine import generate_atlas_stream
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_rag_stream(
    user_query: str,
    request_id: str = None,
):
    logger.info(f"[RAG SERVICE] Query received | query={user_query[:60]}")

    # Step 1: Search similar chunks
    context_df = search_similar_chunks(
    user_query,
    top_k=5,
)

    if context_df is None or len(context_df) == 0:

        logger.warning("[RAG SERVICE] No strong context found")

        def empty_stream():
            yield "data: Not found in the course content\n\n"
            yield "data: [DONE]\n\n"

        return empty_stream()

    logger.info(f"[RAG SERVICE] Context retrieved | chunks={len(context_df)}")

    logger.info("[RAG SERVICE] Starting AtlasAI stream")

    # row = context_df.iloc[0]

    # title = str(row["title"])
    # number = str(row["number"])
    # timestamp = str(row["timestamp"])

    return generate_atlas_stream(
        context_df=context_df,
        query=user_query,
        request_id=request_id,
    )

