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
ECHO_DEFAULT_MODEL = "llama3:latest"
ECHO_FAST_MODEL = "phi3:mini"
ECHO_SMART_MODEL = "qwen3.5:9b"
ATLAS_MODEL = "llama3:latest"

# -------------------- ECHOAI --------------------
def generate_echo_response(messages: list, speed: str = "default") -> str:
    """
    EchoAI — General purpose
    speed = "default" → llama3:latest
    speed = "fast"    → phi3:mini
    speed = "smart"   → qwen3.5:9b
    """
    if speed == "fast":
        model = ECHO_FAST_MODEL
        temperature = 0.6
        max_tokens = 300
    elif speed == "smart":
        model = ECHO_SMART_MODEL
        temperature = 0.8
        max_tokens = 500
    else:
        model = ECHO_DEFAULT_MODEL
        temperature = 0.7
        max_tokens = 500

    logger.info(f"[ECHOAI] Model={model} | Speed={speed} | Messages={len(messages)}")

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
    AtlasAI — RAG based
    Uses llama3:latest with course context
    """
    try:
        prompt = f"""I am teaching web development using Sigma web development course. 
Here are relevant video subtitle chunks:

{context_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}

---------------------------------
Question: "{query}"

Instructions:
- Answer in a human-friendly way
- Mention video number and timestamp
- Guide user to the correct video
- If unrelated to course, say you only answer course-related questions
"""
        logger.info(f"[ATLASAI] Sending RAG prompt | query={query[:60]}")

        r = requests.post(f"{settings.OLLAMA_BASE_URL}/api/generate", json={
            "model": ATLAS_MODEL,
            "prompt": prompt,
            "stream": False
        })

        response = r.json()["response"]
        logger.info(f"[ATLASAI] Response generated | preview={response[:60]}")
        return response

    except Exception as e:
        logger.error(f"[ATLASAI] Error: {str(e)}")
        return f"Error generating RAG response: {str(e)}"