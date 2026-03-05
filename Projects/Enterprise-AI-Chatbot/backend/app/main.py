from fastapi import FastAPI
from backend.app.api import routes

app = FastAPI(title="Enterprise AI Chatbot", version="1.0.0")

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Enterprise AI Chatbot API"}
