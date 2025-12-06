"""
Export API endpoints for downloading generated files.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from loguru import logger

from app.core.config import settings
from app.models.schemas import ExportRequest, ExportResponse
from app.api.extraction import job_storage

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/download/{job_id}")
async def download_results(job_id: str):
    """
    Download the generated Excel file for a completed job.
    
    - **job_id**: Job ID from extraction
    
    Returns Excel file for download.
    """
    try:
        if job_id not in job_storage:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job_data = job_storage[job_id]
        output_path = job_data.get("output_file_path")
        
        if not output_path:
            raise HTTPException(
                status_code=404,
                detail="No output file available. Job may not have completed or consolidation was disabled."
            )
        
        file_path = Path(output_path)
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Output file not found")
        
        logger.info(f"Serving download for job {job_id}: {file_path}")
        
        return FileResponse(
            path=file_path,
            filename=file_path.name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.get("/download/{job_id}/csv")
async def download_results_csv(job_id: str):
    """
    Download results as CSV (if Excel file exists, converts to CSV).
    
    - **job_id**: Job ID from extraction
    
    Returns CSV file for download.
    """
    try:
        if job_id not in job_storage:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job_data = job_storage[job_id]
        output_path = job_data.get("output_file_path")
        
        if not output_path:
            raise HTTPException(status_code=404, detail="No output file available")
        
        xlsx_path = Path(output_path)
        
        # Check if CSV version already exists
        csv_path = xlsx_path.with_suffix('.csv')
        
        if not csv_path.exists():
            # Convert Excel to CSV
            import pandas as pd
            df = pd.read_excel(xlsx_path, sheet_name=0)
            df.to_csv(csv_path, index=False)
            logger.info(f"Converted Excel to CSV: {csv_path}")
        
        return FileResponse(
            path=csv_path,
            filename=csv_path.name,
            media_type="text/csv"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading CSV: {e}")
        raise HTTPException(status_code=500, detail=f"CSV download failed: {str(e)}")


@router.get("/info/{job_id}")
async def get_export_info(job_id: str):
    """
    Get information about available export files.
    
    - **job_id**: Job ID from extraction
    
    Returns file information and download URLs.
    """
    try:
        if job_id not in job_storage:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job_data = job_storage[job_id]
        output_path = job_data.get("output_file_path")
        
        if not output_path:
            return {
                "available": False,
                "message": "No export file available"
            }
        
        file_path = Path(output_path)
        
        if not file_path.exists():
            return {
                "available": False,
                "message": "Export file not found"
            }
        
        file_stat = file_path.stat()
        
        return {
            "available": True,
            "job_id": job_id,
            "filename": file_path.name,
            "file_size": file_stat.st_size,
            "format": "xlsx",
            "download_url": f"/export/download/{job_id}",
            "csv_download_url": f"/export/download/{job_id}/csv"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting export info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get info: {str(e)}")


@router.get("/list")
async def list_exports():
    """
    List all available export files.
    
    Returns list of available downloads.
    """
    try:
        output_dir = Path(settings.output_dir)
        
        if not output_dir.exists():
            return {"exports": [], "total": 0}
        
        exports = []
        
        for file_path in output_dir.glob("*.xlsx"):
            file_stat = file_path.stat()
            
            # Try to extract job ID from filename
            job_id = file_path.stem.replace("_results", "")
            
            exports.append({
                "filename": file_path.name,
                "job_id": job_id,
                "file_size": file_stat.st_size,
                "created_at": file_stat.st_ctime,
                "download_url": f"/export/download/{job_id}"
            })
        
        # Sort by creation time (newest first)
        exports.sort(key=lambda x: x["created_at"], reverse=True)
        
        return {"exports": exports, "total": len(exports)}
        
    except Exception as e:
        logger.error(f"Error listing exports: {e}")
        raise HTTPException(status_code=500, detail=f"List failed: {str(e)}")
