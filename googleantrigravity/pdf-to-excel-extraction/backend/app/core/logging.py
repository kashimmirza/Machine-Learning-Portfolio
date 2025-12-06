"""
Logging configuration using loguru for structured logging.
"""

from loguru import logger
from pathlib import Path
import sys
from app.core.config import settings


def setup_logging():
    """Configure logging with loguru."""
    
    # Remove default handler
    logger.remove()
    
    # Add console handler with color
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )
    
    # Add file handler for all logs
    log_path = Path(settings.log_dir) / "app.log"
    logger.add(
        log_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
    )
    
    # Add separate file handler for errors
    error_log_path = Path(settings.log_dir) / "errors.log"
    logger.add(
        error_log_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="5 MB",
        retention="60 days",
        compression="zip",
    )
    
    logger.info(f"{settings.app_name} v{settings.app_version} - Logging initialized")
    return logger


# Initialize logging
app_logger = setup_logging()
