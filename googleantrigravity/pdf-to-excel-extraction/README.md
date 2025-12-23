# PDF to Excel Extraction Application

AI-powered document extraction system that converts PDF invoices and utility bills into structured Excel/CSV outputs.

## 🚀 Features

- **Multi-file Upload**: Drag-and-drop interface for uploading multiple PDF files
- **AI-Powered Extraction**: Uses GPT-4 Vision for intelligent data extraction
- **OCR Fallback**: Tesseract OCR for cost-effective processing
- **Smart Document Detection**: Automatically identifies document types (invoices, utility bills)
- **Data Consolidation**: Merges multiple documents into a single Excel file
- **Professional Formatting**: Clean, formatted Excel output with summaries
- **Real-time Progress**: Live status updates during processing
- **Dual Export**: Download as Excel (XLSX) or CSV

## 📋 Requirements

### Backend
- Python 3.9+
- pip

### Frontend
- Node.js 18+
- npm or yarn

### Optional (for advanced OCR)
- OpenAI API key (for GPT-4 Vision)
- Tesseract OCR (free alternative)

## 🛠️ Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd pdf-to-excel-extraction/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Install Tesseract OCR:
```bash
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# Mac: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr
```

6. Install poppler for PDF to image conversion:
```bash
# Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases
# Mac: brew install poppler
# Linux: sudo apt-get install poppler-utils
```

7. Copy `.env.example` to `.env` and configure:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

8. Edit `.env` and add your OpenAI API key (optional):
```
OPENAI_API_KEY=your_api_key_here
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd pdf-to-excel-extraction/frontend
```

2. Install dependencies:
```bash
npm install
```

## 🚀 Running the Application

### Start Backend

```bash
cd backend
python -m app.main
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

### Start Frontend

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:5173`

## 📖 Usage

1. **Upload PDFs**: Drag and drop or click to select PDF files
2. **Configure**: Choose document type (or auto-detect) and consolidation options
3. **Process**: Click "Start Extraction" and watch real-time progress
4. **Download**: Get your Excel or CSV file with extracted data

## 🎯 Supported Document Types

### Invoices
- Invoice number, date, due date
- Supplier/customer information
- Subtotal, tax, total amounts
- Line items and descriptions
- Reference numbers

### Utility Bills
- Account number
- Billing period
- Consumption (kWh, m³, etc.)
- Meter readings
- Charges and totals
- Provider information

## 📁 Project Structure

```
pdf-to-excel-extraction/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration & logging
│   │   ├── models/       # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── utils/        # Helper functions
│   ├── uploads/          # Temporary file storage
│   ├── outputs/          # Generated Excel files
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API client
│   │   └── App.jsx       # Main application
│   └── package.json
└── README.md
```

## 🔧 Configuration

### Backend (.env)

- `OPENAI_API_KEY`: OpenAI API key for GPT-4 Vision
- `OCR_PROVIDER`: Primary OCR provider (gpt4vision, tesseract)
- `MAX_UPLOAD_SIZE_MB`: Maximum file upload size (default: 50MB)
- `MAX_FILES_PER_UPLOAD`: Maximum files per upload (default: 20)
- `CORS_ORIGINS`: Allowed CORS origins
- `DEBUG`: Enable debug mode

See `.env.example` for all available options.

## 📊 API Endpoints

### Upload
- `POST /upload/`: Upload PDF files
- `GET /upload/list`: List uploaded files
- `DELETE /upload/{file_id}`: Delete uploaded file

### Extraction
- `POST /extract/start`: Start extraction job
- `GET /extract/status/{job_id}`: Check job status
- `GET /extract/result/{job_id}`: Get extraction results
- `DELETE /extract/{job_id}`: Delete job

### Export
- `GET /export/download/{job_id}`: Download Excel file
- `GET /export/download/{job_id}/csv`: Download as CSV
- `GET /export/info/{job_id}`: Get export file info
- `GET /export/list`: List all exports

## 🐳 Docker Deployment (Coming Soon)

```bash
docker-compose up -d
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔒 Security Considerations

- API keys stored in environment variables
- File upload validation (type, size)
- CORS configuration for frontend access
- Temporary file cleanup
- Input sanitization

## 💰 Cost Estimation

### GPT-4 Vision
- Approximately $0.01-0.03 per page
- High accuracy for complex documents

### Tesseract OCR
- Free and open-source
- Lower accuracy for complex layouts
- Good for simple text-based documents

## 📝 Future Enhancements

- [ ] User authentication and accounts
- [ ] File management dashboard
- [ ] Template learning and customization
- [ ] Batch processing queue
- [ ] Email notifications
- [ ] Analytics and reporting
- [ ] Multi-language support
- [ ] Cloud storage integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is proprietary software developed for consultancy services.

## 📧 Support

For support, please contact your project administrator.

## 🙏 Acknowledgments

- OpenAI GPT-4 Vision API
- Tesseract OCR
- FastAPI framework
- React and Vite
- All open-source contributors
