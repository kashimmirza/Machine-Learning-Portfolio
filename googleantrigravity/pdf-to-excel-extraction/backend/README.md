# Backend - PDF to Excel Extraction API

FastAPI-based backend for AI-powered PDF data extraction.

## Architecture

### Services Layer
- **PDF Processor**: Text extraction and image conversion
- **OCR Service**: GPT-4 Vision and Tesseract integration
- **Extractor**: Main extraction orchestration
- **Consolidator**: Multi-document data merging
- **Excel Generator**: Professional Excel/CSV output

### API Endpoints

#### Upload (`/upload`)
- Multi-file upload with validation
- File management and listing

#### Extraction (`/extract`)
- Background job processing
- Real-time status updates
- Result retrieval

#### Export (`/export`)
- Excel/CSV downloads
- File information and listing

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the server:
```bash
python -m app.main
```

4. Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Running with hot reload:
```bash
uvicorn app.main:app --reload
```

### Running tests:
```bash
pytest tests/ -v
```

### Code formatting:
```bash
black app/
isort app/
```

## Configuration

See `.env.example` for all configuration options.

### Key Settings:
- `OPENAI_API_KEY`: Required for GPT-4 Vision
- `OCR_PROVIDER`: gpt4vision or tesseract
- `MAX_UPLOAD_SIZE_MB`: File upload limit
- `DEBUG`: Enable debug mode

## Logging

Logs are written to:
- `logs/app.log`: All logs with rotation
- `logs/errors.log`: Error-level logs only
- Console: INFO and above

## Dependencies

Core dependencies:
- FastAPI: Web framework
- OpenAI: GPT-4 Vision API
- pdfplumber: PDF text extraction
- pytesseract: OCR fallback
- pandas: Data manipulation
- openpyxl: Excel generation

See `requirements.txt` for complete list.
