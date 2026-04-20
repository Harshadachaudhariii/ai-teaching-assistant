# services/chat_service.py
# EchoAI Service

from core.llm_engine import generate_echo_response
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_chat_response(messages: list, speed: str = "default") -> str:
    """
    speed = "default" → llama3:latest  (balanced)
    speed = "fast"    → phi3:mini      (quick)
    speed = "smart"   → llama3         (deep — same as default but higher tokens)
    """
    logger.info(f"[CHAT SERVICE] Request | speed={speed} | messages={len(messages)}")

    response = generate_echo_response(messages, speed)

    logger.info(f"[CHAT SERVICE] Response ready | preview={response[:60]}")
    return response