"""
File upload API endpoints.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from pathlib import Path
from datetime import datetime
from loguru import logger

from app.core.config import settings
from app.models.schemas import UploadResponse, UploadedFile, ErrorResponse
from app.utils.helpers import generate_file_id, clean_filename

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/", response_model=UploadResponse)
async def upload_files(
    files: List[UploadFile] = File(..., description="PDF files to upload")
):
    """
    Upload multiple PDF files for processing.
    
    - **files**: List of PDF files (max 20 files, 50MB each)
    
    Returns upload confirmation with file IDs.
    """
    try:
        # Validate number of files
        if len(files) > settings.max_files_per_upload:
            raise HTTPException(
                status_code=400,
                detail=f"Too many files. Maximum {settings.max_files_per_upload} files allowed."
            )
        
        if not files:
            raise HTTPException(
                status_code=400,
                detail="No files provided"
            )
        
        uploaded_files = []
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            # Validate file type
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid file type: {file.filename}. Only PDF files are allowed."
                )
            
            # Read file content
            content = await file.read()
            file_size = len(content)
            
            # Validate file size
            if file_size > settings.max_upload_size_bytes:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large: {file.filename}. Maximum size is {settings.max_upload_size_mb}MB."
                )
            
            if file_size == 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Empty file: {file.filename}"
                )
            
            # Generate file ID and save
            file_id = generate_file_id()
            clean_name = clean_filename(file.filename)
            save_path = upload_dir / f"{file_id}_{clean_name}"
            
            # Write file to disk
            with open(save_path, "wb") as f:
                f.write(content)
            
            # Create uploaded file record
            uploaded_file = UploadedFile(
                file_id=file_id,
                filename=clean_name,
                file_size=file_size,
                upload_time=datetime.now()
            )
            
            uploaded_files.append(uploaded_file)
            
            logger.info(f"File uploaded: {clean_name} ({file_size} bytes) - ID: {file_id}")
        
        return UploadResponse(
            success=True,
            files=uploaded_files,
            message=f"Successfully uploaded {len(uploaded_files)} file(s)"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading files: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """
    Delete an uploaded file.
    
    - **file_id**: ID of the file to delete
    """
    try:
        upload_dir = Path(settings.upload_dir)
        
        # Find file with matching ID
        matching_files = list(upload_dir.glob(f"{file_id}_*"))
        
        if not matching_files:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Delete file
        for file_path in matching_files:
            file_path.unlink()
            logger.info(f"Deleted file: {file_path}")
        
        return {"success": True, "message": "File deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


@router.get("/list")
async def list_uploaded_files():
    """
    List all uploaded files.
    
    Returns list of uploaded files with metadata.
    """
    try:
        upload_dir = Path(settings.upload_dir)
        
        if not upload_dir.exists():
            return {"files": []}
        
        files = []
        for file_path in upload_dir.glob("*.pdf"):
            # Extract file ID from filename (format: {file_id}_{original_name})
            parts = file_path.name.split("_", 1)
            if len(parts) == 2:
                file_id, original_name = parts
            else:
                file_id = file_path.stem
                original_name = file_path.name
            
            file_stat = file_path.stat()
            
            files.append({
                "file_id": file_id,
                "filename": original_name,
                "file_size": file_stat.st_size,
                "upload_time": datetime.fromtimestamp(file_stat.st_mtime)
            })
        
        return {"files": files, "total": len(files)}
        
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail=f"List failed: {str(e)}")
