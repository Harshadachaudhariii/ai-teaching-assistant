# core/llm_engine.py
from openai import OpenAI
import requests
from core.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------- CLIENT (EchoAI) --------------------
client = OpenAI(
    base_url=f"{settings.OLLAMA_BASE_URL}/v1",
    api_key="ollama",
)
logger.info(f"[LLM ENGINE] Client initialized at {settings.OLLAMA_BASE_URL}")

# -------------------- MODELS --------------------
ECHO_DEFAULT_MODEL = "llama3:latest"   # default — balanced
ECHO_FAST_MODEL    = "phi3:mini"       # fast    — quick
ECHO_SMART_MODEL   = "llama3:latest"   # smart   — same model, more tokens
ATLAS_MODEL        = "llama3:latest"   # RAG

# -------------------- ECHOAI --------------------
def generate_echo_response(messages: list, speed: str = "default") -> str:
    """
    EchoAI speed modes:
    default -> llama3:latest  (balanced)
    fast    -> phi3:mini      (quick)
    smart   -> llama3:latest  (deep — higher tokens)
    """
    if speed == "fast":
        model, temperature, max_tokens = ECHO_FAST_MODEL, 0.6, 400
    elif speed == "smart":
        model, temperature, max_tokens = ECHO_SMART_MODEL, 0.7, 2000
    else:  # default
        model, temperature, max_tokens = ECHO_DEFAULT_MODEL, 0.7, 600

    logger.info(f"[ECHOAI] Speed={speed} | Model={model} | MaxTokens={max_tokens} | Messages={len(messages)}")

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        full_response = ""
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                full_response += delta.content

        logger.info(f"[ECHOAI] Response generated | preview={full_response[:60]}")
        return full_response

    except Exception as e:
        logger.error(f"[ECHOAI] Error: {str(e)}")
        return f"Error generating response: {str(e)}"


# -------------------- ATLASAI --------------------
def generate_atlas_response(context_df, query: str) -> str:
    """
    AtlasAI RAG — improved prompt from process_incoming.py
    Timestamps already MM:SS from vector_store
    """
    try:
        context_json = context_df[
            ["title", "number", "start", "end", "text"]
        ].to_json(orient="records")

        prompt = f"""You are an AI teaching assistant for a web development course.

You are given multiple video transcript chunks.

Context:
{context_json}

----------------------------------
Question: "{query}"
---------------------------------

Instructions:

1. Read all context carefully.
2. Choose the most relevant video.
3. Ignore unrelated content.
4. Explain WHAT the concept is and WHY it is used (3-4 lines).
5. Do NOT copy raw text.
6. The explanation MUST define the concept clearly.
7. If no relevant info reply exactly: "Not found in the course content"
8. Return ONLY ONE answer.
9. Never include raw context, scores, or debug info.

---------------------------------

Output (STRICT - follow exactly):

<Short explanation>

Video: <number> (<title>)
Timestamp: <MM:SS>

Do NOT include anything else.
"""
        logger.info(f"[ATLASAI] Sending RAG prompt | query={query[:60]}")

        r = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": ATLAS_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 250,
                }
            },
            timeout=90
        )

        response = r.json().get("response", "").strip()
        logger.info(f"[ATLASAI] Response generated | preview={response[:60]}")
        return response

    except Exception as e:
        logger.error(f"[ATLASAI] Error: {str(e)}")
        return f"Error generating RAG response: {str(e)}"