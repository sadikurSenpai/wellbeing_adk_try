from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.api.models.chat_schema import ChatRequest
from app.service.chat.chat_service import generate_chat_stream, get_or_create_session

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        session_id = await get_or_create_session(request.user_id, request.session_id)
        
        return StreamingResponse(
            generate_chat_stream(
                user_id=request.user_id,
                message=request.message,
                session_id=session_id
            ),
            media_type="text/plain",
            headers={"X-Session-ID": session_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
