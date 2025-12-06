"""
OCR service with multiple provider support.
Primary: Google Gemini for intelligent extraction
Fallback: Tesseract for offline/cost-saving
"""

import base64
import json
from io import BytesIO
from typing import Dict, Any, Optional, List
from PIL import Image
import pytesseract
import google.generativeai as genai
from loguru import logger
from app.core.config import settings
from app.models.extraction_fields import create_extraction_prompt


class OCRService:
    """OCR service with multiple provider support."""
    
    def __init__(self):
        self.provider = settings.ocr_provider
        self.fallback_provider = settings.fallback_ocr
        self.timeout = settings.ocr_timeout_seconds
        self.max_retries = settings.max_retries
        
        # Initialize Gemini client if API key is available
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.gemini_model = genai.GenerativeModel(settings.gemini_model)
            logger.success(f"Gemini API initialized with model: {settings.gemini_model}")
        else:
            self.gemini_model = None
            logger.warning("Gemini API key not set - Gemini Vision will not be available")
    
    def extract_data(
        self,
        image: Image.Image,
        document_type: str = "invoice",
        custom_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Extract structured data from image using configured OCR provider.
        
        Args:
            image: PIL Image object
            document_type: Type of document (invoice, utility_bill)
            custom_fields: Optional custom fields to extract
        
        Returns:
            Dictionary of extracted fields
        """
        try:
            # Try primary provider
            if self.provider == "gemini" and self.gemini_model:
                result = self._extract_with_gemini(image, document_type, custom_fields)
                if result:
                    return result
                logger.warning("Gemini extraction failed, falling back to tesseract")
            
            # Fallback to tesseract
            if self.fallback_provider == "tesseract":
                return self._extract_with_tesseract(image, document_type)
            
            logger.error("All OCR providers failed")
            return {}
            
        except Exception as e:
            logger.error(f"Error in OCR extraction: {e}")
            return {}
    
    def _extract_with_gemini(
        self,
        image: Image.Image,
        document_type: str,
        custom_fields: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Extract data using Google Gemini Vision API.
        
        Args:
            image: PIL Image object
            document_type: Type of document
            custom_fields: Optional custom fields
        
        Returns:
            Extracted data dictionary or None if failed
        """
        try:
            if not self.gemini_model:
                logger.error("Gemini client not initialized")
                return None
            
            logger.info(f"Extracting data with Gemini Vision - Document type: {document_type}")
            
            # Create extraction prompt
            prompt = create_extraction_prompt(document_type, custom_fields)
            
            # Call Gemini Vision API
            response = self.gemini_model.generate_content([prompt, image])
            
            # Parse response
            content = response.text
            logger.debug(f"Gemini Vision raw response: {content}")
            
            # Extract JSON from response
            extracted_data = self._parse_json_response(content)
            
            if extracted_data:
                logger.success(f"Successfully extracted {len(extracted_data)} fields with Gemini Vision")
                return extracted_data
            else:
                logger.warning("Failed to parse Gemini Vision response")
                return None
                
        except Exception as e:
            logger.error(f"Error with Gemini Vision extraction: {e}")
            return None
    
    def _extract_with_tesseract(
        self,
        image: Image.Image,
        document_type: str
    ) -> Dict[str, Any]:
        """
        Extract text using Tesseract OCR.
        This is a basic extraction - returns raw text.
        
        Args:
            image: PIL Image object
            document_type: Type of document
        
        Returns:
            Dictionary with raw text
        """
        try:
            logger.info("Extracting text with Tesseract OCR")
            
            # Extract text
            text = pytesseract.image_to_string(image)
            
            logger.success(f"Tesseract extracted {len(text)} characters")
            
            # Return raw text - basic parsing could be added here
            return {
                "raw_text": text,
                "extraction_method": "tesseract",
                "note": "Basic text extraction - may require manual parsing"
            }
            
        except Exception as e:
            logger.error(f"Error with Tesseract extraction: {e}")
            return {
                "error": str(e),
                "extraction_method": "tesseract_failed"
            }
    
    def _parse_json_response(self, content: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON from API response.
        Handles cases where API includes extra text.
        
        Args:
            content: Raw response content
        
        Returns:
            Parsed JSON dictionary or None
        """
        try:
            # Try direct JSON parse
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code block
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_str = content[json_start:json_end].strip()
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
            
            # Try to find JSON object in content
            try:
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    return json.loads(json_str)
            except json.JSONDecodeError:
                pass
            
            logger.error(f"Failed to parse JSON from response: {content[:200]}")
            return None
    
    def extract_from_text(
        self,
        text: str,
        document_type: str = "invoice",
        custom_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Extract structured data from plain text using Gemini.
        
        Args:
            text: Extracted text from PDF
            document_type: Type of document
            custom_fields: Optional custom fields
        
        Returns:
            Dictionary of extracted fields
        """
        try:
            if not self.gemini_model:
                logger.error("Gemini client not initialized")
                return {"raw_text": text}
            
            logger.info(f"Extracting data from text with Gemini - Document type: {document_type}")
            
            # Create extraction prompt
            prompt = create_extraction_prompt(document_type, custom_fields)
            full_prompt = f"{prompt}\n\nDocument text:\n{text}"
            
            # Call Gemini API
            response = self.gemini_model.generate_content(full_prompt)
            
            # Parse response
            content = response.text
            extracted_data = self._parse_json_response(content)
            
            if extracted_data:
                logger.success(f"Successfully extracted {len(extracted_data)} fields from text")
                return extracted_data
            else:
                logger.warning("Failed to parse Gemini response")
                return {"raw_text": text}
                
        except Exception as e:
            logger.error(f"Error extracting from text: {e}")
            return {"raw_text": text}


# Global instance
ocr_service = OCRService()
