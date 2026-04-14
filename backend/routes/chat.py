# routes/chat.py
# routes/chat.py

from fastapi import APIRouter, HTTPException
from services.chat_service import generate_chat_response

router = APIRouter()

@router.post("/")
async def chat_endpoint(data: dict):
    """
    Expected Input:
    {
        "messages": [
            {"role": "user", "content": "Hello"}
        ],
        "speed": "default"  # "default" = llama3 | "fast" = phi3:mini
    }
    """

    try:
        messages = data.get("messages", [])
        speed = data.get("speed", "default")  # ← changed from mode to speed

        if not messages:
            raise HTTPException(status_code=400, detail="Messages required")

        response = generate_chat_response(messages, speed)  # ← pass speed

        return {"response": response}

    except Exception as e:
        return {"error": str(e)}