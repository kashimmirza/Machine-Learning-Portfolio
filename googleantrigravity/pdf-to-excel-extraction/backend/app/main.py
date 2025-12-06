"""
FastAPI main application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.config import settings
from app.core.logging import app_logger
from app.api import upload, extraction, export


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown."""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"OCR Provider: {settings.ocr_provider}")
    
    # Ensure directories exist
    settings.ensure_directories()
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered PDF to Excel extraction service for invoices and utility bills",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(upload.router)
app.include_router(extraction.router)
app.include_router(export.router)


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs_url": "/docs",
        "description": "PDF to Excel extraction API",
        "endpoints": {
            "upload": "/upload/",
            "extract": "/extract/start",
            "status": "/extract/status/{job_id}",
            "result": "/extract/result/{job_id}",
            "download": "/export/download/{job_id}",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "details": str(exc) if settings.debug else None
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
