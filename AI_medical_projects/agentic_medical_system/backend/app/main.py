from contextlib import asynccontextmanager
from typing import Dict, Any
from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.core.config import settings
from app.core.logging import logger
from app.core.metrics import setup_metrics
from app.core.middleware import LoggingContextMiddleware, MetricsMiddleware
from app.core.limiter import limiter
from app.api.v1.api import api_router
from app.services.database import database_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Startup: {settings.PROJECT_NAME} v{settings.VERSION}")
    # Initialize MongoDB
    from app.core.mongo_db import mongo_db
    await mongo_db.connect()
    yield
    # Close resources
    await mongo_db.close()
    logger.info("Shutdown")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# 1. Metrics
setup_metrics(app)

# 2. Middleware
app.add_middleware(LoggingContextMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 4. Routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["health"][0])
async def health_check(request: Request) -> Dict[str, Any]:
    db_healthy = await database_service.health_check()
    status_code = status.HTTP_200_OK if db_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if db_healthy else "degraded",
            "components": {
                "api": "healthy",
                "database": "healthy" if db_healthy else "unhealthy"
            },
            "timestamp": datetime.now().isoformat()
        }
    )

@app.get("/")
async def root():
    return {
        "name": settings.PROJECT_NAME, 
        "version": settings.VERSION,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
