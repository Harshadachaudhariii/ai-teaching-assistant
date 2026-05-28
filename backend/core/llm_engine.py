# core/llm_engine.py

import threading
import time
import uuid
import json
from openai import OpenAI
import requests as http_requests
from typing import Generator, Optional
from core.config import settings
from utils.logger import get_logger
import re

logger = get_logger(__name__)

client = OpenAI(base_url=f"{settings.OLLAMA_BASE_URL}/v1", api_key="ollama")

ECHO_DEFAULT_MODEL = "llama3:latest"
ECHO_FAST_MODEL    = "phi3:mini"
ECHO_SMART_MODEL   = "llama3:latest"
ATLAS_MODEL        = "llama3:latest"

# ── SPEED CONFIG ─────────────────────────────────────────────
SPEED_CONFIG = {
    "fast":    (ECHO_FAST_MODEL,    0.3,  600,  90),
    "default": (ECHO_DEFAULT_MODEL, 0.4,  1500, 150),
    "smart":   (ECHO_SMART_MODEL,   0.4,  2500, 180),
}

MAX_HISTORY_MESSAGES = 8    # 4 user + 4 assistant turns

ECHO_SYSTEM_PROMPT = """
You are EchoAI.

IMPORTANT RESPONSE RULES:

1. ALL programming code MUST be inside markdown code fences.

2. ALWAYS use this exact format:

```language
code here
```
3. NEVER place code inline with normal text.
4. ALWAYS preserve:
indentation
spaces
blank lines
line breaks
5. NEVER compress code into a single line.
6. Add a blank line before and after every code block.
7. Explanations and code must be separated clearly.
8. This rule applies to ALL languages:
Python
JavaScript
Java
C
C++
HTML
CSS
SQL
Bash
JSON
YAML
every other language
9. NEVER output:
python#
javascript#
cpp#
10. ALWAYS output proper fenced markdown blocks.
"""
def _build_messages(messages: list) -> list:
    """
    Trim history and inject formatting system prompt.
    """

    non_system = [
        m for m in messages
        if m.get("role") != "system"
    ]

    trimmed = non_system[-MAX_HISTORY_MESSAGES:]

    return [
        {
            "role": "system",
            "content": ECHO_SYSTEM_PROMPT
        },
        *trimmed
    ]


# ── Cancel registry ──────────────────────────────────────────
_cancel_events: dict[str, threading.Event] = {}
_registry_lock = threading.Lock()

def register_request(request_id: str) -> threading.Event:
    event = threading.Event()
    with _registry_lock:
        _cancel_events[request_id] = event
    return event

def cancel_request(request_id: str) -> bool:
    with _registry_lock:
        event = _cancel_events.get(request_id)
    if event:
        event.set()
        logger.info(f"[LLM ENGINE] Cancel signalled | req={request_id}")
        return True
    return False

def unregister_request(request_id: str):
    with _registry_lock:
        _cancel_events.pop(request_id, None)


# ── EchoAI streaming generator ───────────────────────────────
def generate_echo_stream(
    messages: list,
    speed: str = "default",
    request_id: Optional[str] = None,
) -> Generator[str, None, None]:
    """
    Yields raw text tokens directly from Ollama for EchoAI.
    No modifications, system prompts, or regex filters applied.
    """
    if speed not in SPEED_CONFIG:
        speed = "default"

    model, temperature, max_tokens, hard_timeout = SPEED_CONFIG[speed]

    if request_id is None:
        request_id = "echo-" + str(uuid.uuid4())

    with _registry_lock:
        cancel_event: Optional[threading.Event] = _cancel_events.get(request_id)

    built_messages = _build_messages(messages)

    logger.info(
        f"[LLM ENGINE] Stream start | speed={speed} model={model} "
        f"max_tok={max_tokens} msgs={len(built_messages)} req={request_id}"
    )

    stream = None
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=built_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            timeout=60,
        )

        start_time = time.time()

        for chunk in stream:
            if time.time() - start_time > hard_timeout:
                logger.error(f"[LLM ENGINE] Hard timeout {hard_timeout}s | req={request_id}")
                try:
                    stream.close()
                except Exception:
                    pass
                return

            if cancel_event and cancel_event.is_set():
                logger.info(f"[LLM ENGINE] Cancelled mid-stream | req={request_id}")
                try:
                    stream.close()
                except Exception:
                    pass
                return

            try:
                delta   = chunk.choices[0].delta
                content = getattr(delta, "content", None)
                
                # Directly yield the raw token content exactly as the model speaks it
                if content:
                    yield content

            except Exception:
                continue

        logger.info(f"[LLM ENGINE] Stream complete | req={request_id}")

    except GeneratorExit:
        logger.info(f"[LLM ENGINE] GeneratorExit | req={request_id}")
        if stream:
            try:
                stream.close()
            except Exception:
                logger.warning("[LLM ENGINE] Stream close failed")

    except Exception as e:
        logger.error(f"[LLM ENGINE] Stream error: {e} | req={request_id}")
        yield f"[Error: {str(e)}]"

    finally:
        if request_id:
            unregister_request(request_id)


def generate_echo_response(messages: list, speed: str = "default") -> str:
    """Collects full stream natively with zero text adjustments."""
    return "".join(generate_echo_stream(messages, speed))


# ─────────────────────────────────────────────────────────────
# AtlasAI — UNTOUCHED below this line
# ─────────────────────────────────────────────────────────────

ATLAS_SYSTEM_PROMPT = """
You are AtlasAI, an AI teaching assistant for web development courses.

Answer the user's question ONLY using the provided course context.


STRICT RULES:
1. Use ONLY the provided context.
2. Never hallucinate or invent information.
3. Return ONLY:
   - Video Title
   - Video Number
   - Timestamp
4. Do NOT add introductions or conclusions.
5. Do NOT use bullet points.
6. Do NOT use markdown.
7. Do NOT output JSON or XML.
8. Do NOT repeat the user's question.
9. Keep output clean and minimal.
10. If the answer is not found in the context, respond exactly with:
Not found in course content

EXAMPLE OUTPUT:

Video Title: CSS Box Model - Margin, Padding & Borders
Video Number: 18
Timestamp: 07:06


You are AtlasAI, an AI teaching assistant specialized in searching video transcripts.
Analyze the provided course context chunks and determine which chunk contains the answer to the user's question.

STRICT RULES:
1. Output ONLY the index number of the matching chunk (e.g., 0, 1, 2, etc.).
2. If the answer is not found in any of the chunks, output exactly: -1
3. Do NOT include any introductory or concluding text, punctuation, or markdown.
"""

def build_atlas_prompt(context_df, query: str) -> tuple[str, dict]:
    context_lines = []
    
    # We create clean layout maps for the LLM to inspect
    for idx, row in context_df.iterrows():
        context_lines.append(
            f"--- CHUNK INDEX: {idx} ---\n"
            f"Transcript Content:\n{str(row['text'])[:1200]}"
        )

    context_block = "\n\n".join(context_lines)

    prompt = (
        f"CONTEXT CHUNKS:\n{context_block}\n\n"
        f"QUESTION: {query}\n\n"
        f"Output the single matching chunk index or -1:"
    )

    # Cache iloc[0] metadata as a reliable fallback in case parsing fails
    best = context_df.iloc[0]
    fallback_meta = {
        "title":     str(best.get("title", "Unknown Title")),
        "number":    str(best.get("number", "N/A")),
        "timestamp": str(best.get("timestamp", "00:00")),
    }

    return prompt, fallback_meta

def generate_atlas_stream(
    context_df,
    query: str,
    request_id: Optional[str] = None,
) -> Generator[str, None, None]:

    if request_id is None:
        request_id = "atlas-" + str(uuid.uuid4())

    try:
        prompt, fallback_meta = build_atlas_prompt(context_df, query)
        logger.info(f"[ATLASAI] Processing request | req={request_id}")

        # Get prediction index decision from Ollama
        response = client.chat.completions.create(
            model=ATLAS_MODEL,
            messages=[
                {"role": "system", "content": ATLAS_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            stream=False,
            temperature=0.0
        )

        raw_decision = response.choices[0].message.content.strip()
        logger.info(f"[ATLASAI] Raw LLM output: '{raw_decision}' | req={request_id}")

        # --- RESILIENT PARSING LAYER ---
        # Look for the first integer sequence in the model's text response
        match = re.search(r'-?\d+', raw_decision)
        
        if match:
            chosen_index = int(match.group())
        else:
            chosen_index = -2  # Force to fallback track if no integer found

        logger.info(f"[ATLASAI] Parsed Index Match: {chosen_index} | req={request_id}")

        # Check if index exists inside the dataframe tracking frame
        if 0 <= chosen_index < len(context_df):
            row = context_df.iloc[chosen_index]
            title = str(row.get("title", fallback_meta["title"]))
            number = str(row.get("number", fallback_meta["number"]))
            timestamp = str(row.get("timestamp", fallback_meta["timestamp"]))
        else:
            # SAFETY FALLBACK: Instead of displaying 'Not found', revert back to the highest score row
            logger.warning(f"[ATLASAI] Index validation missed. Using best chunk row fallback.")
            title = fallback_meta["title"]
            number = fallback_meta["number"]
            timestamp = fallback_meta["timestamp"]

        # Stream directly out to the frontend client app UI layout format lines
        yield f"data: Video Title: {title}\n\n"
        yield f"data: Video Number: {number}\n\n"
        yield f"data: Timestamp: {timestamp}\n\n"
        yield "data: [DONE]\n\n"

    except Exception as e:
        logger.error(f"[ATLASAI] Stream error: {e} | req={request_id}")
        yield f"data: [Error: {str(e)}]\n\n"
        yield "data: [DONE]\n\n"