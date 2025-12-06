"""
Main extraction service that orchestrates PDF processing and OCR.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

from app.services.pdf_processor import pdf_processor
from app.services.ocr_service import ocr_service
from app.models.schemas import DocumentType, DocumentExtraction, ExtractedField


class Extractor:
    """Main extraction service."""
    
    def __init__(self):
        self.pdf_processor = pdf_processor
        self.ocr_service = ocr_service
    
    def extract_from_file(
        self,
        file_path: str,
        file_id: str,
        document_type: str = "invoice",
        custom_fields: Optional[List[str]] = None
    ) -> DocumentExtraction:
        """
        Extract data from a single PDF file.
        
        Args:
            file_path: Path to PDF file
            file_id: Unique file identifier
            document_type: Type of document (invoice, utility_bill)
            custom_fields: Optional custom fields to extract
        
        Returns:
            DocumentExtraction object with results
        """
        try:
            logger.info(f"Starting extraction for file: {file_path}")
            filename = Path(file_path).name
            
            # Check if PDF is scanned or text-based
            is_scanned = self.pdf_processor.is_scanned_pdf(file_path)
            
            extracted_data = {}
            
            if is_scanned:
                # Convert to images and use OCR
                logger.info("PDF is scanned - using image-based extraction")
                extracted_data = self._extract_from_scanned_pdf(
                    file_path, document_type, custom_fields
                )
            else:
                # Extract text and use text-based extraction
                logger.info("PDF is text-based - using text extraction")
                extracted_data = self._extract_from_text_pdf(
                    file_path, document_type, custom_fields
                )
            
            # Convert extracted data to ExtractedField objects
            fields = []
            for field_name, value in extracted_data.items():
                fields.append(ExtractedField(
                    field_name=field_name,
                    value=value,
                    confidence=None  # Could add confidence scoring
                ))
            
            # Detect document type if not specified
            detected_type = self._detect_document_type(extracted_data)
            if document_type == "unknown":
                document_type = detected_type
            
            result = DocumentExtraction(
                file_id=file_id,
                filename=filename,
                document_type=DocumentType(document_type),
                fields=fields,
                extraction_time=datetime.now(),
                success=bool(extracted_data and extracted_data.get("error") is None),
                error=extracted_data.get("error")
            )
            
            logger.success(f"Successfully extracted {len(fields)} fields from {filename}")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting from file {file_path}: {e}")
            return DocumentExtraction(
                file_id=file_id,
                filename=Path(file_path).name,
                document_type=DocumentType.UNKNOWN,
                fields=[],
                extraction_time=datetime.now(),
                success=False,
                error=str(e)
            )
    
    def _extract_from_scanned_pdf(
        self,
        file_path: str,
        document_type: str,
        custom_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Extract data from scanned PDF using OCR."""
        try:
            # Convert to images
            images = self.pdf_processor.convert_to_images(file_path)
            
            if not images:
                return {"error": "Failed to convert PDF to images"}
            
            # For multi-page documents, we'll process the first page
            # (could be enhanced to process all pages and merge results)
            first_page = images[0]
            
            # Extract data using OCR
            extracted_data = self.ocr_service.extract_data(
                first_page, document_type, custom_fields
            )
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"Error extracting from scanned PDF: {e}")
            return {"error": str(e)}
    
    def _extract_from_text_pdf(
        self,
        file_path: str,
        document_type: str,
        custom_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Extract data from text-based PDF."""
        try:
            # Extract text
            text = self.pdf_processor.extract_text(file_path)
            
            if not text:
                return {"error": "Failed to extract text from PDF"}
            
            # Use OCR service to extract structured data from text
            extracted_data = self.ocr_service.extract_from_text(
                text, document_type, custom_fields
            )
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"Error extracting from text PDF: {e}")
            return {"error": str(e)}
    
    def _detect_document_type(self, extracted_data: Dict[str, Any]) -> str:
        """
        Detect document type based on extracted fields.
        
        Args:
            extracted_data: Dictionary of extracted fields
        
        Returns:
            Detected document type
        """
        # Simple heuristic - could be improved with ML
        invoice_indicators = ["invoice_number", "supplier_name", "total_amount"]
        utility_indicators = ["account_number", "consumption", "meter_reading"]
        
        invoice_score = sum(1 for field in invoice_indicators if field in extracted_data)
        utility_score = sum(1 for field in utility_indicators if field in extracted_data)
        
        if invoice_score > utility_score:
            return "invoice"
        elif utility_score > invoice_score:
            return "utility_bill"
        else:
            return "unknown"


# Global instance
extractor = Extractor()
