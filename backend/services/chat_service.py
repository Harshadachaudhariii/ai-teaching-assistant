# services/chat_service.py
# EchoAI Service

# services/chat_service.py
# EchoAI Service

from core.llm_engine import generate_echo_response
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_chat_response(messages: list, speed: str = "default") -> str:
    logger.info(f"[CHAT SERVICE] Request | speed={speed} | messages={len(messages)}")

    response = generate_echo_response(messages, speed)

    logger.info(f"[CHAT SERVICE] Response ready | preview={response[:60]}")
    return response