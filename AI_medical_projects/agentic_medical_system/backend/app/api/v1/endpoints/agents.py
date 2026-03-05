from fastapi import APIRouter, HTTPException
from typing import Any, Dict
from app.agents.orchestrator import agent_orchestrator
from pydantic import BaseModel

router = APIRouter()

class AgentRequest(BaseModel):
    agent_type: str  # "vitals" or "nutrition"
    data: Dict[str, Any]

@router.post("/chat", response_model=Dict[str, Any])
async def chat_with_agents(request: AgentRequest):
    """
    Direct interaction with the Multi-Agent System.
    """
    result = await agent_orchestrator.route_request(request.agent_type, request.data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/broadcast", response_model=Dict[str, Any])
async def broadcast_to_agents(data: Dict[str, Any]):
    """
    Send data to all agents for a comprehensive check.
    """
    return await agent_orchestrator.broadcast(data)
