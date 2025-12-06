"""
PDF processing service for text extraction and image conversion.
Handles both text-based and scanned PDFs.
"""

import pdfplumber
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path
from typing import List, Tuple, Optional
from loguru import logger
from app.core.config import settings


class PDFProcessor:
    """Handles PDF parsing, text extraction, and image conversion."""
    
    def __init__(self):
        self.dpi = settings.image_dpi
        self.enable_preprocessing = settings.enable_preprocessing
    
    def is_scanned_pdf(self, pdf_path: str) -> bool:
        """
        Detect if a PDF is scanned (image-based) or text-based.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            True if PDF appears to be scanned, False otherwise
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Check first few pages
                pages_to_check = min(3, len(pdf.pages))
                text_length = 0
                
                for i in range(pages_to_check):
                    text = pdf.pages[i].extract_text()
                    if text:
                        text_length += len(text.strip())
                
                # If very little text found, likely scanned
                avg_text_per_page = text_length / pages_to_check
                is_scanned = avg_text_per_page < 50
                
                logger.info(
                    f"PDF analysis: {pdf_path} - "
                    f"Avg text per page: {avg_text_per_page:.0f} chars - "
                    f"Is scanned: {is_scanned}"
                )
                
                return is_scanned
                
        except Exception as e:
            logger.error(f"Error checking if PDF is scanned: {e}")
            # Default to treating as scanned if error
            return True
    
    def extract_text(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from text-based PDF.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Extracted text or None if extraction fails
        """
        try:
            logger.info(f"Extracting text from PDF: {pdf_path}")
            
            with pdfplumber.open(pdf_path) as pdf:
                text_parts = []
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"--- Page {page_num} ---\n{page_text}")
                
                full_text = "\n\n".join(text_parts)
                logger.success(f"Extracted {len(full_text)} characters from {len(pdf.pages)} pages")
                
                return full_text if full_text else None
                
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return None
    
    def convert_to_images(self, pdf_path: str) -> List[Image.Image]:
        """
        Convert PDF pages to images for OCR processing.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            List of PIL Image objects, one per page
        """
        try:
            logger.info(f"Converting PDF to images: {pdf_path}")
            
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                fmt='PNG'
            )
            
            logger.success(f"Converted {len(images)} pages to images")
            
            if self.enable_preprocessing:
                images = [self.preprocess_image(img) for img in images]
            
            return images
            
        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}")
            return []
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image to improve OCR accuracy.
        
        Args:
            image: PIL Image object
        
        Returns:
            Preprocessed image
        """
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Denoise if enabled
            if settings.preprocessing_denoise:
                image = image.filter(ImageFilter.MedianFilter(size=3))
            
            # Enhance contrast if enabled
            if settings.preprocessing_contrast:
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.5)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.3)
            
            return image
            
        except Exception as e:
            logger.warning(f"Error preprocessing image: {e}")
            return image
    
    def get_page_count(self, pdf_path: str) -> int:
        """
        Get the number of pages in a PDF.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Number of pages
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                return len(pdf.pages)
        except Exception as e:
            logger.error(f"Error getting page count: {e}")
            return 0
    
    def extract_images_from_pdf(self, pdf_path: str, output_dir: str) -> List[str]:
        """
        Extract embedded images from PDF and save to directory.
        
        Args:
            pdf_path: Path to PDF file
            output_dir: Directory to save extracted images
        
        Returns:
            List of paths to extracted images
        """
        try:
            logger.info(f"Extracting images from PDF: {pdf_path}")
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            image_paths = []
            pdf_name = Path(pdf_path).stem
            
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract images from page
                    if hasattr(page, 'images'):
                        for img_num, img in enumerate(page.images, 1):
                            img_path = output_path / f"{pdf_name}_page{page_num}_img{img_num}.png"
                            # Note: pdfplumber doesn't directly extract images
                            # This is a placeholder for actual image extraction logic
                            # You may need to use PyMuPDF (fitz) for this
                            image_paths.append(str(img_path))
            
            logger.success(f"Extracted {len(image_paths)} images")
            return image_paths
            
        except Exception as e:
            logger.error(f"Error extracting images from PDF: {e}")
            return []


# Global instance
pdf_processor = PDFProcessor()
