"""
Extraction API endpoints for processing PDFs.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from loguru import logger
import asyncio

from app.core.config import settings
from app.models.schemas import (
    ExtractionRequest,
    ExtractionStatus,
    ExtractionResult,
    JobStatus,
    DocumentExtraction
)
from app.services.extractor import extractor
from app.services.consolidator import consolidator
from app.services.excel_generator import excel_generator
from app.utils.helpers import generate_job_id

router = APIRouter(prefix="/extract", tags=["extraction"])

# In-memory storage for job status (could be replaced with Redis/database)
job_storage: Dict[str, Dict] = {}


@router.post("/start", response_model=ExtractionStatus)
async def start_extraction(
    request: ExtractionRequest,
    background_tasks: BackgroundTasks
):
    """
    Start extraction process for uploaded files.
    
    - **file_ids**: List of uploaded file IDs to process
    - **document_type**: Type of documents (invoice, utility_bill, or unknown for auto-detect)
    - **custom_fields**: Optional list of additional fields to extract
    - **consolidate**: Whether to consolidate results into single Excel file
    
    Returns job ID and initial status. Use /extract/status/{job_id} to check progress.
    """
    try:
        if not request.file_ids:
            raise HTTPException(status_code=400, detail="No file IDs provided")
        
        # Validate files exist
        upload_dir = Path(settings.upload_dir)
        file_paths = []
        
        for file_id in request.file_ids:
            matching_files = list(upload_dir.glob(f"{file_id}_*"))
            if not matching_files:
                raise HTTPException(status_code=404, detail=f"File not found: {file_id}")
            file_paths.append(matching_files[0])
        
        # Generate job ID
        job_id = generate_job_id()
        
        # Initialize job status
        job_storage[job_id] = {
            "job_id": job_id,
            "status": JobStatus.PENDING,
            "progress": 0.0,
            "files_processed": 0,
            "total_files": len(file_paths),
            "current_file": None,
            "started_at": datetime.now(),
            "completed_at": None,
            "error_message": None,
            "extractions": [],
            "file_ids": request.file_ids,
            "document_type": request.document_type.value,
            "custom_fields": request.custom_fields,
            "consolidate": request.consolidate,
        }
        
        # Start background processing
        background_tasks.add_task(
            process_extraction_job,
            job_id,
            file_paths,
            request
        )
        
        logger.info(f"Started extraction job: {job_id} with {len(file_paths)} files")
        
        return ExtractionStatus(
            job_id=job_id,
            status=JobStatus.PENDING,
            progress=0.0,
            files_processed=0,
            total_files=len(file_paths),
            started_at=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting extraction: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start extraction: {str(e)}")


@router.get("/status/{job_id}", response_model=ExtractionStatus)
async def get_extraction_status(job_id: str):
    """
    Get the current status of an extraction job.
    
    - **job_id**: Job ID returned from /extract/start
    
    Returns current processing status and progress.
    """
    try:
        if job_id not in job_storage:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job_data = job_storage[job_id]
        
        return ExtractionStatus(
            job_id=job_data["job_id"],
            status=job_data["status"],
            progress=job_data["progress"],
            files_processed=job_data["files_processed"],
            total_files=job_data["total_files"],
            current_file=job_data.get("current_file"),
            started_at=job_data["started_at"],
            completed_at=job_data.get("completed_at"),
            error_message=job_data.get("error_message")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@router.get("/result/{job_id}", response_model=ExtractionResult)
async def get_extraction_result(job_id: str):
    """
    Get the results of a completed extraction job.
    
    - **job_id**: Job ID returned from /extract/start
    
    Returns extracted data and output file path if available.
    """
    try:
        if job_id not in job_storage:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job_data = job_storage[job_id]
        
        if job_data["status"] not in [JobStatus.COMPLETED, JobStatus.FAILED]:
            raise HTTPException(
                status_code=400,
                detail=f"Job not completed. Current status: {job_data['status']}"
            )
        
        extractions = job_data.get("extractions", [])
        successful = sum(1 for e in extractions if e.success)
        failed = len(extractions) - successful
        
        return ExtractionResult(
            job_id=job_id,
            status=job_data["status"],
            documents=extractions,
            total_processed=len(extractions),
            successful=successful,
            failed=failed,
            output_file_path=job_data.get("output_file_path")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job result: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get result: {str(e)}")


async def process_extraction_job(
    job_id: str,
    file_paths: list,
    request: ExtractionRequest
):
    """
    Background task to process extraction job.
    
    Args:
        job_id: Unique job identifier
        file_paths: List of file paths to process
        request: Extraction request parameters
    """
    try:
        job_storage[job_id]["status"] = JobStatus.PROCESSING
        extractions = []
        
        for idx, file_path in enumerate(file_paths):
            try:
                # Update status
                job_storage[job_id]["current_file"] = file_path.name
                
                logger.info(f"Processing file {idx + 1}/{len(file_paths)}: {file_path.name}")
                
                # Extract data from file
                extraction = extractor.extract_from_file(
                    str(file_path),
                    request.file_ids[idx],
                    request.document_type.value,
                    request.custom_fields
                )
                
                extractions.append(extraction)
                
                # Update progress
                job_storage[job_id]["files_processed"] = idx + 1
                job_storage[job_id]["progress"] = ((idx + 1) / len(file_paths)) * 100
                
                # Small delay to prevent overwhelming the API
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
                # Create failed extraction record
                extraction = DocumentExtraction(
                    file_id=request.file_ids[idx],
                    filename=file_path.name,
                    document_type=request.document_type,
                    fields=[],
                    extraction_time=datetime.now(),
                    success=False,
                    error=str(e)
                )
                extractions.append(extraction)
        
        # Store extractions
        job_storage[job_id]["extractions"] = extractions
        
        # Consolidate and generate Excel if requested
        if request.consolidate and extractions:
            try:
                logger.info(f"Consolidating {len(extractions)} extractions")
                
                # Consolidate data
                df = consolidator.consolidate(extractions)
                
                if not df.empty:
                    # Calculate summary
                    summary = consolidator.calculate_summary(df)
                    
                    # Generate Excel file
                    output_filename = f"{job_id}_results"
                    output_path = excel_generator.generate_excel(
                        df,
                        output_filename,
                        include_summary=True,
                        summary_data=summary
                    )
                    
                    job_storage[job_id]["output_file_path"] = output_path
                    logger.success(f"Generated Excel file: {output_path}")
                else:
                    logger.warning("No data to consolidate")
                    
            except Exception as e:
                logger.error(f"Error consolidating/generating Excel: {e}")
                job_storage[job_id]["error_message"] = f"Consolidation failed: {str(e)}"
        
        # Mark as completed
        job_storage[job_id]["status"] = JobStatus.COMPLETED
        job_storage[job_id]["completed_at"] = datetime.now()
        job_storage[job_id]["progress"] = 100.0
        
        logger.success(f"Extraction job completed: {job_id}")
        
    except Exception as e:
        logger.error(f"Fatal error in extraction job {job_id}: {e}")
        job_storage[job_id]["status"] = JobStatus.FAILED
        job_storage[job_id]["error_message"] = str(e)
        job_storage[job_id]["completed_at"] = datetime.now()


@router.delete("/{job_id}")
async def delete_job(job_id: str):
    """
    Delete a job and its associated data.
    
    - **job_id**: Job ID to delete
    """
    try:
        if job_id not in job_storage:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Delete output file if it exists
        output_path = job_storage[job_id].get("output_file_path")
        if output_path:
            Path(output_path).unlink(missing_ok=True)
        
        # Remove from storage
        del job_storage[job_id]
        
        logger.info(f"Deleted job: {job_id}")
        
        return {"success": True, "message": "Job deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job: {e}")
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
