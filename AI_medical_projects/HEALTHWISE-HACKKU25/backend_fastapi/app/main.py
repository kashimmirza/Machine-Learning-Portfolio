from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.mongo import db
from app.core.security import get_current_user
from app.agents.orchestrator import orchestrator
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# CORS (Allow Host Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Strict production setting: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.close()

@app.get("/")
async def root():
    return {"message": "HealthWise Agentic Backend Active"}

# Agent Request Model
class AgentRequest(BaseModel):
    agent_type: str
    data: Dict[str, Any]

@app.post("/api/agents/chat")
async def agent_chat(request: AgentRequest, user = Depends(get_current_user)):
    """
    Protected Agent Chat Endpoint
    """
    if not user:
         # For Dev testing purposes, strict auth might be disabled or mocked
         pass 

    result = await orchestrator.route_request(request.agent_type, request.data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
