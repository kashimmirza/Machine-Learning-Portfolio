from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "HealthWise Agentic Backend"
    API_V1_STR: str = "/api"
    
    # Database (Shared with Node)
    MONGODB_URI: str = "mongodb://localhost:27017" # Default fallback
    DB_NAME: str = "prescripto"
    
    # Security (Must match Node backend)
    JWT_SECRET: str = "your_jwt_secret" # Will read from env
    ALGORITHM: str = "HS256"
    
    # AI Config
    GEMINI_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file="../backend/.env", # Read from sibling directory
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
