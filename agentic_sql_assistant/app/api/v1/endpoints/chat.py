from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any
from app.core.agent.graph import app_graph
from langchain_core.messages import HumanMessage
import json
import asyncio

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str

@router.post("/message")
async def chat_message(request: ChatRequest):
    """
    Standard HTTP endpoint for chat. Returns the final response.
    """
    inputs = {"messages": [HumanMessage(content=request.message)]}
    # config = {"configurable": {"thread_id": request.session_id}} 
    # State persistence is handled by Checkpointer in full implementation,
    # for MVP we just run the graph.
    
    output = await app_graph.ainvoke(inputs)
    final_message = output['messages'][-1]
    return {"response": final_message.content}

async def stream_generator(message: str):
    inputs = {"messages": [HumanMessage(content=message)]}
    async for event in app_graph.astream_events(inputs, version="v1"):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                yield f"data: {json.dumps({'content': content})}\n\n"
        elif kind == "on_tool_start":
            yield f"data: {json.dumps({'status': 'Executing SQL query...'})}\n\n"

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming endpoint using SSE.
    """
    return StreamingResponse(
        stream_generator(request.message),
        media_type="text/event-stream"
    )
