from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import contact, health

app = FastAPI(
    title="ContinuousCare API",
    description="Backend API for ContinuousCare website",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(contact.router, prefix="/api", tags=["contact"])

@app.get("/")
async def root():
    return {"message": "ContinuousCare API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
