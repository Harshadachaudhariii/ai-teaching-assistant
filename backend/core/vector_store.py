# vector_store.py
import numpy as np
import re
import requests
from sklearn.metrics.pairwise import cosine_similarity
from core.embeddings_loader import embeddings_df
from utils.logger import get_logger
from core.config import settings

logger = get_logger(__name__)

# -------------------- CONFIG --------------------
SIMILARITY_THRESHOLD = 0.55   # improved precision
TOP_K = 5                       # final chunks sent to LLM
MAX_PER_VIDEO = 3         # allow 2 chunks per video max

# -------------------- EMBEDDING --------------------
def create_embedding(text_list: list) -> list:
    try:
        logger.info(f"[VECTOR STORE] Embedding query | {text_list[0][:60]}")

        r = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/embed",
            json={
                "model": "bge-m3",
                "input": text_list
            }
        )

        embeddings = r.json()["embeddings"]
        logger.info("[VECTOR STORE] Embedding created successfully")
        return embeddings

    except Exception as e:
        logger.error(f"[VECTOR STORE] Embedding error: {str(e)}")
        return []


# -------------------- FORMAT TIME --------------------
def format_time(seconds: float) -> str:
    try:
        total = int(float(seconds))
        return f"{total // 60:02d}:{total % 60:02d}"
    except:
        return "00:00"

def estimate_relevant_timestamp(text, query, start_sec, end_sec):

    try:

        text_lower = text.lower()

        query_words = [
            w for w in query.lower().split()
            if len(w) > 2
        ]

        if not query_words:
            return format_time(start_sec)

        # split transcript into windows
        words = text_lower.split()

        window_size = 20

        best_score = 0
        best_index = 0

        for i in range(0, len(words), 5):

            window = " ".join(words[i:i + window_size])

            score = 0

            for q in query_words:

                if q in window:
                    score += 1

            if score > best_score:
                best_score = score
                best_index = i

        ratio = best_index / max(len(words), 1)

        estimated_sec = (
            float(start_sec) +
            (float(end_sec) - float(start_sec)) * ratio
        )

        return format_time(estimated_sec)

    except:
        return format_time(start_sec)

# -------------------- SEARCH --------------------
def search_similar_chunks(query: str, top_k: int = TOP_K):
    try:
        if embeddings_df is None:
            logger.warning("[VECTOR STORE] Embeddings not loaded")
            return None

        # 1. Query embedding
        question_embedding = create_embedding([query])[0]

        # 2. Similarity calculation
        # 2. Similarity calculation
        embeddings_matrix = np.vstack(embeddings_df["embedding"].values)

        similarities = cosine_similarity(
            embeddings_matrix,
            [question_embedding]
        ).flatten()

        # -------------------------------------------------
        # Dynamic keyword boosting
        # Helps retrieve chunks closer to actual teaching
        # timestamps without hardcoding topics/videos
        # -------------------------------------------------

        query_lower = query.lower()

        # extract meaningful query words
        query_keywords = re.findall(r"\b[a-zA-Z]{3,}\b", query_lower)

        # remove weak/common words
        stopwords = {
            "what", "is", "how", "why", "when",
            "where", "the", "and", "for",
            "about", "explain", "tell",
            "show", "give", "can", "you",
            "this", "that", "with"
        }

        keywords = [
            word for word in query_keywords
            if word not in stopwords
        ]

        # boost chunks containing exact keywords
        for i in range(len(similarities)):

            text = str(embeddings_df.iloc[i]["text"]).lower()

            boost = 0

            for kw in keywords:

                # exact word matching only
                if re.search(rf"\b{re.escape(kw)}\b", text):
                    boost += 0.05

            similarities[i] += boost

        # 3. Filter by threshold
        filtered_idx = [
            i for i, score in enumerate(similarities)
            if score >= SIMILARITY_THRESHOLD
        ]

        if not filtered_idx:
            logger.warning(f"[VECTOR STORE] No matches above {SIMILARITY_THRESHOLD}")
            return None

        # 4. Sort by similarity
        query_lower = query.lower()

        def keyword_score(text, title):

            score = 0

            combined = f"{title} {text}".lower()

            query_words = [
                w for w in query_lower.split()
                if len(w) > 2
            ]

            # reward keyword presence
            for word in query_words:

                if re.search(rf"\b{re.escape(word)}\b", combined):
                    score += 1
            # exact phrase boost
            if query_lower in combined:
                score += 15
            # strong boost if keyword in title
            for word in query_words:

                if word in title.lower():
                    score += 8

            return score


        sorted_indices = sorted(
            filtered_idx,
            key=lambda i: (

                # embedding similarity
                similarities[i] * 0.85 +

                # keyword/title relevance
                keyword_score(
                    str(embeddings_df.iloc[i]["text"]),
                    str(embeddings_df.iloc[i]["title"])
                ) * 0.10 +

                # slight preference for longer chunks
                min(len(str(embeddings_df.iloc[i]["text"])), 400) / 400 * 0.05
            ),
            reverse=True
        )

        # 5. Deduplicate with max per video logic
        seen_texts = set()
        video_counts = {}
        final_indices = []

        for idx in sorted_indices:
            row = embeddings_df.iloc[idx]

            text = str(row["text"]).strip().lower()
            video_number = row["number"]

            # duplicate text skip
            if text in seen_texts:
                continue

            # max 2 chunks per video
            count = video_counts.get(video_number, 0)
            if count >= MAX_PER_VIDEO:
                continue

            seen_texts.add(text)
            video_counts[video_number] = count + 1

            final_indices.append(idx)

            if len(final_indices) >= top_k:
                break

        if not final_indices:
            logger.warning("[VECTOR STORE] No valid chunks after filtering")
            return None

        # 6. Build result dataframe
        result_df = embeddings_df.loc[final_indices].copy()
        result_df = result_df.reset_index(drop=True)
        # attach scores
        result_df["score"] = [
            float(similarities[i]) for i in final_indices
        ]

        # prioritize chunks whose timestamps
        # format timestamps first
        result_df["timestamp"] = result_df["start"].apply(format_time)

        # prioritize chunks whose timestamps
        # are not extremely close to video start
        # truncate text for LLM context
        result_df["text"] = result_df["text"].apply(lambda x: str(x)[:700])

        # 7. Logging
        for i in final_indices:
            logger.info(
                f"[VECTOR STORE] Match | "
                f"score={similarities[i]:.4f} | "
                f"video={embeddings_df.iloc[i]['number']} | "
                f"title={embeddings_df.iloc[i]['title'][:50]}"
            )

        logger.info(f"[VECTOR STORE] Retrieved {len(result_df)} chunks")
        print("\n\n========== TOP RESULTS ==========")

        for _, row in result_df.iterrows():

            print({
                "video": row["number"],
                "title": row["title"],
                "timestamp": row["timestamp"],
                "score": row["score"],
                "text": str(row["text"])[:120]
            })

        print("=================================\n\n")
        return result_df

    except Exception as e:
        logger.error(f"[VECTOR STORE] Search error: {str(e)}")
        return None