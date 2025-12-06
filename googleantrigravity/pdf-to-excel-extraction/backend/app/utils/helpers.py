"""
Utility helper functions.
"""

import uuid
from pathlib import Path
from typing import Optional
from datetime import datetime
import hashlib


def generate_file_id() -> str:
    """Generate a unique file ID."""
    return str(uuid.uuid4())


def generate_job_id() -> str:
    """Generate a unique job ID."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"job_{timestamp}_{unique_id}"


def get_file_hash(file_path: str) -> str:
    """
    Calculate SHA256 hash of a file.
    
    Args:
        file_path: Path to file
    
    Returns:
        Hexadecimal hash string
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def clean_filename(filename: str) -> str:
    """
    Clean and sanitize a filename.
    
    Args:
        filename: Original filename
    
    Returns:
        Cleaned filename
    """
    # Remove path components
    filename = Path(filename).name
    
    # Replace invalid characters
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename


def ensure_extension(filename: str, extension: str) -> str:
    """
    Ensure filename has the correct extension.
    
    Args:
        filename: Filename to check
        extension: Required extension (with or without dot)
    
    Returns:
        Filename with correct extension
    """
    if not extension.startswith('.'):
        extension = f".{extension}"
    
    path = Path(filename)
    if path.suffix.lower() != extension.lower():
        return str(path.with_suffix(extension))
    return filename
