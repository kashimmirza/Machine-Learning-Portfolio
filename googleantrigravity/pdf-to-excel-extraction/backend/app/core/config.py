"""
Application configuration management using pydantic-settings.
Loads configuration from environment variables and .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # API Configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    
    # Azure (Optional)
    azure_form_recognizer_key: str = ""
    azure_form_recognizer_endpoint: str = ""
    
    # AWS (Optional)
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    
    # Application
    app_name: str = "PDF to Excel Extraction"
    app_version: str = "1.0.0"
    debug: bool = True
    log_level: str = "INFO"
    
    # File Upload
    max_upload_size_mb: int = 50
    allowed_extensions: str = ".pdf"
    max_files_per_upload: int = 20
    
    # Storage Paths
    upload_dir: str = "./uploads"
    output_dir: str = "./outputs"
    log_dir: str = "./logs"
    
    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # OCR Settings
    ocr_provider: str = "gemini"  # gemini, tesseract, azure, aws
    fallback_ocr: str = "tesseract"
    ocr_timeout_seconds: int = 30
    max_retries: int = 3
    
    # Processing
    enable_preprocessing: bool = True
    image_dpi: int = 300
    preprocessing_denoise: bool = True
    preprocessing_contrast: bool = True
    
    # Rate Limiting
    rate_limit_requests_per_minute: int = 60
    rate_limit_enabled: bool = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def max_upload_size_bytes(self) -> int:
        """Convert MB to bytes."""
        return self.max_upload_size_mb * 1024 * 1024
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse allowed extensions into a list."""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        Path(self.upload_dir).mkdir(parents=True, exist_ok=True)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

# Ensure directories exist on import
settings.ensure_directories()
