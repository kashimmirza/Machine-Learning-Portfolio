from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Nutrify 2.0 API", lifespan=lifespan)

from .api import recognition, foods, auth

app.include_router(recognition.router, prefix="/api/recognition", tags=["recognition"])
app.include_router(foods.router, prefix="/api/foods", tags=["foods"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Nutrify 2.0 API"}
