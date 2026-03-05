from fastapi import APIRouter
from app.api.v1 import auth, chatbot, analysis

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
from app.api.v1.endpoints import agents
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
