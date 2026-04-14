# routes/rag.py

from fastapi import APIRouter
from services.rag_service import generate_rag_response

router = APIRouter()

@router.post("/")
async def rag_endpoint(data: dict):
    try:
        query = data.get("query")

        if not query:
            return {"error": "Query is required"}

        response = generate_rag_response(query)

        return {"response": response}

    except Exception as e:
        return {"error": f"RAG Error: {str(e)}"}