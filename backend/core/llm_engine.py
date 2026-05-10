# core/llm_engine.py
# ─────────────────────────────────────────────────────────────
# Thread-safe cancellation using threading.Event.
# When cancelled, stream.close() is called immediately —
# this closes the HTTP connection to Ollama so it stops
# generating even if the client disconnected.
# ─────────────────────────────────────────────────────────────

import threading
import uuid
from openai import OpenAI
import requests as http_requests
from typing import Generator, Optional
from core.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

client = OpenAI(base_url=f"{settings.OLLAMA_BASE_URL}/v1", api_key="ollama")

ECHO_DEFAULT_MODEL = "llama3:latest"
ECHO_FAST_MODEL    = "phi3:mini"
ECHO_SMART_MODEL   = "llama3:latest"
ATLAS_MODEL        = "llama3:latest"

# ─────────────────────────────────────────────────────────────
# Global cancel registry
# { request_id: threading.Event }
# Event is set() to signal cancellation.
# ─────────────────────────────────────────────────────────────
_cancel_events: dict[str, threading.Event] = {}
_registry_lock = threading.Lock()


def register_request(request_id: str) -> threading.Event:
    """Create and store a cancel event for this request."""
    event = threading.Event()
    with _registry_lock:
        _cancel_events[request_id] = event
    return event


def cancel_request(request_id: str) -> bool:
    """Signal cancellation. Returns True if request was found."""
    with _registry_lock:
        event = _cancel_events.get(request_id)
    if event:
        event.set()
        logger.info(f"[LLM ENGINE] Cancel signalled | req={request_id}")
        return True
    return False


def unregister_request(request_id: str):
    """Remove from registry after completion or cancel."""
    with _registry_lock:
        _cancel_events.pop(request_id, None)


# ─────────────────────────────────────────────────────────────
# EchoAI — cancellable streaming generator
# ─────────────────────────────────────────────────────────────
def generate_echo_stream(
    
    messages: list,
    speed: str = "default",
    request_id: Optional[str] = None,
) -> Generator[str, None, None]:
    """
    Yields text chunks.
    If request_id is given, checks its cancel event before each chunk.
    Calls stream.close() to immediately stop Ollama generation on cancel.
    """
    if speed not in ["default", "fast", "smart"]:
        speed = "default"
    if speed == "fast":
        model, temperature, max_tokens = ECHO_FAST_MODEL, 0.6, 400
    elif speed == "smart":
        model, temperature, max_tokens = ECHO_SMART_MODEL, 0.7, 2000
    else:
        model, temperature, max_tokens = ECHO_DEFAULT_MODEL, 0.7, 600

    cancel_event: Optional[threading.Event] = None
    if request_id is None:
        request_id = "unknown-" + str(uuid.uuid4())

    logger.info(f"[LLM ENGINE] Stream start | speed={speed} model={model} req={request_id}")

    stream = None
    try:
        stream = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=temperature,
    max_tokens=max_tokens,
    stream=True,
    timeout=60,   # ADD THIS
)
        import time
        start_time = time.time()
        for chunk in stream:
            if time.time() - start_time > 120:
                logger.error("[LLM ENGINE] Hard timeout reached")
                try:
                    stream.close()
                except Exception:
                    pass
                return
            # ── Check cancel before yielding each token ──
            if cancel_event and cancel_event.is_set():
                logger.info(f"[LLM ENGINE] Cancelled mid-stream | req={request_id}")
                try:
                    stream.close()   # closes HTTP connection → Ollama stops
                except Exception:
                    pass
                return   # StopIteration — generator ends cleanly

            try:
                delta = chunk.choices[0].delta
                content = getattr(delta, "content", None)

                if content:
                    yield content

            except Exception:
                continue

        logger.info(f"[LLM ENGINE] Stream complete | req={request_id}")

    except GeneratorExit:
        # Client disconnected (e.g. browser tab closed)
        logger.info(f"[LLM ENGINE] GeneratorExit | req={request_id}")
        if stream:
            try:
                if stream:
                    stream.close()
            except Exception:
                logger.warning("[LLM ENGINE] Stream close failed")

    except Exception as e:
        logger.error(f"[LLM ENGINE] Stream error: {e} | req={request_id}")
        yield f"[Error: {str(e)}]"

    finally:
        if request_id:
            unregister_request(request_id)


# ─────────────────────────────────────────────────────────────
# Non-streaming wrapper (title generation, RAG)
# ─────────────────────────────────────────────────────────────
def generate_echo_response(messages: list, speed: str = "default") -> str:
    """Collects full stream — no cancel support (short requests only)."""
    return "".join(generate_echo_stream(messages, speed))


# ─────────────────────────────────────────────────────────────
# AtlasAI — RAG (non-streaming, Ollama /api/generate)
# ─────────────────────────────────────────────────────────────
def generate_atlas_response(context_df, query: str) -> str:
    try:
        context_json = context_df[
            ["title", "number", "start", "end", "text"]
        ].to_json(orient="records")

        prompt = f"""You are an AI teaching assistant for a web development course.
Context: {context_json}
Question: "{query}"
Instructions: Explain WHAT and WHY (3–4 lines). If no relevant info reply exactly: "Not found in the course content"
Output (strict):
<Short explanation>
Video: <number> (<title>)
Timestamp: <MM:SS>"""

        r = http_requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model":  ATLAS_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 300},
            },
            timeout=90,
        )
        return r.json().get("response", "").strip()

    except Exception as e:
        logger.error(f"[ATLASAI] Error: {e}")
        return f"Error: {str(e)}"