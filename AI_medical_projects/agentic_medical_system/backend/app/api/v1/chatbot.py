from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
import json
import uuid

from app.api.v1.auth import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse, StreamResponse
from app.core.langgraph.graph import LangGraphAgent
from app.core.limiter import limiter
from app.core.config import settings

router = APIRouter()
agent = LangGraphAgent()

@router.post("/chat", response_model=ChatResponse)
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["chat"][0])
async def chat(
    request: Request,
    chat_request: ChatRequest,
    user: User = Depends(get_current_user)
):
    # For now generating a session ID per request if not provided
    # Ideally should be passed in headers or body
    session_id = str(uuid.uuid4()) 
    
    result = await agent.get_response(
        chat_request.messages,
        session_id=session_id,
        user_id=str(user.id)
    )
    # Convert result to Message schemas
    # result is list of dicts from dump_messages
    return ChatResponse(messages=result)

@router.post("/chat/stream")
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["chat_stream"][0])
async def chat_stream(
    request: Request,
    chat_request: ChatRequest,
    user: User = Depends(get_current_user)
):
    session_id = str(uuid.uuid4())
    
    async def event_generator():
        try:
            async for chunk in agent.get_stream_response(
                chat_request.messages,
                session_id=session_id,
                user_id=str(user.id)
            ):
                response = StreamResponse(content=chunk, done=False)
                yield f"data: {json.dumps(response.model_dump())}\n\n"
            
            final = StreamResponse(content="", done=True)
            yield f"data: {json.dumps(final.model_dump())}\n\n"
        except Exception as e:
            err = StreamResponse(content=f"Error: {str(e)}", done=True)
            yield f"data: {json.dumps(err.model_dump())}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
