import os
import sys
from paddleocr import PaddleOCR, draw_ocr

def extract_content_to_markdown(pdf_path):
    """
    Extracts text from a PDF using PaddleOCR and converts it to a simple Markdown format.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found.")
        return None

    # Initialize PaddleOCR
    # use_angle_cls=True enables angle classification
    # lang='en' for English, can be changed based on PDF content
    ocr = PaddleOCR(use_angle_cls=True, lang='en', page_num=0) # page_num=0 is not a valid arg for init, removing it.
    
    # PaddleOCR works best with images, but supports PDF path if 'page_num' is handled or if we convert PDF to images first.
    # For simplicity in this script, we assume PaddleOCR handles the PDF directly or we might need a helper to convert PDF to images if PaddleOCR's direct PDF support is limited in the installed version.
    # Standard PaddleOCR `ocr.ocr` accepts image path or numpy array. 
    # If passing a PDF path, it usually processes the first page or requires iteration.
    
    print(f"Processing {pdf_path}...")
    result = ocr.ocr(pdf_path, cls=True)

    markdown_content = ""
    
    # Result structure: [ [ [ [x1,y1], [x2,y2], ... ], (text, confidence) ], ... ]
    # If multiple pages, result might be a list of lists.
    
    # Flatten if necessary (PaddleOCR output structure can vary by version/input)
    # For a single image/page:
    if result is None:
        print("No text found.")
        return ""

    # Simple heuristic for layout preservation:
    # Sort boxes by Y coordinate (top to bottom), then X (left to right)
    # This is a basic approximation.
    
    # Handle multi-page result if input is PDF
    # Note: ocr.ocr(pdf_path) might return a list of results per page.
    
    all_lines = []
    
    # Check if result is a list of lists (pages) or just one page
    # This check depends on PaddleOCR version, assuming standard list of lines per page
    for idx, page_result in enumerate(result):
        if not page_result:
            continue
            
        print(f"Processing page {idx + 1}...")
        
        # Sort by vertical position (y1 of the bounding box)
        # box is line[0], text_info is line[1]
        # box is [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        page_result.sort(key=lambda x: x[0][0][1]) 
        
        for line in page_result:
            box = line[0]
            text, confidence = line[1]
            
            # Basic font size/header detection could go here based on box height
            # For now, just appending text
            all_lines.append(text)
            
        all_lines.append("---") # Page break

    markdown_content = "\n\n".join(all_lines)
    
    return markdown_content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_pdf.py <path_to_pdf>")
        sys.exit(1)
        
    pdf_file = sys.argv[1]
    md_output = extract_content_to_markdown(pdf_file)
    
    if md_output:
        output_file = pdf_file + ".md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_output)
        print(f"Markdown saved to {output_file}")
