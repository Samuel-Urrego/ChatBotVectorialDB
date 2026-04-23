from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter()

@router.post("/ask")
async def ask_question(request: ChatRequest):
    try:
        print(f"QUESTION RECEIVED: {request.question}")
        return StreamingResponse(
            chat_service.get_answer_stream(request.question),
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
