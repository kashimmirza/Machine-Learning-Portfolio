"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class JobStatus(str, Enum):
    """Job processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentType(str, Enum):
    """Type of document being processed."""
    INVOICE = "invoice"
    UTILITY_BILL = "utility_bill"
    UNKNOWN = "unknown"


class UploadedFile(BaseModel):
    """Uploaded file information."""
    file_id: str
    filename: str
    file_size: int
    upload_time: datetime = Field(default_factory=datetime.now)


class UploadResponse(BaseModel):
    """Response from file upload endpoint."""
    success: bool
    files: List[UploadedFile]
    message: str


class ExtractionRequest(BaseModel):
    """Request to start extraction process."""
    file_ids: List[str]
    document_type: Optional[DocumentType] = DocumentType.UNKNOWN
    custom_fields: Optional[List[str]] = None
    consolidate: bool = True


class ExtractionStatus(BaseModel):
    """Status of extraction job."""
    job_id: str
    status: JobStatus
    progress: float = Field(ge=0, le=100)
    files_processed: int
    total_files: int
    current_file: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class ExtractedField(BaseModel):
    """Single extracted field with confidence."""
    field_name: str
    value: Any
    confidence: Optional[float] = None


class DocumentExtraction(BaseModel):
    """Extracted data from a single document."""
    file_id: str
    filename: str
    document_type: DocumentType
    fields: List[ExtractedField]
    extraction_time: datetime = Field(default_factory=datetime.now)
    success: bool
    error: Optional[str] = None


class ExtractionResult(BaseModel):
    """Complete extraction results."""
    job_id: str
    status: JobStatus
    documents: List[DocumentExtraction]
    total_processed: int
    successful: int
    failed: int
    output_file_path: Optional[str] = None


class ExportRequest(BaseModel):
    """Request to export data to Excel/CSV."""
    job_id: str
    format: str = Field(default="xlsx", pattern="^(xlsx|csv)$")
    include_confidence: bool = False
    sheet_name: Optional[str] = "Extracted Data"


class ExportResponse(BaseModel):
    """Response from export endpoint."""
    success: bool
    file_path: str
    download_url: str
    file_size: int
    message: str


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None
