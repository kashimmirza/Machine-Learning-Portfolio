from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.services.database import init_db
from app.core.metrics import setup_metrics
from app.core.middleware import MetricsMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Initializing Database...")
    try:
        init_db()
        print("Database initialized.")
    except Exception as e:
        print(f"Error initializing DB: {e}")
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# 1. Set up Prometheus metrics
setup_metrics(app)

# 2. Add custom metrics middleware (Tracks latency)
app.add_middleware(MetricsMiddleware)

# 3. CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173", # Vite default
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "ok"}
