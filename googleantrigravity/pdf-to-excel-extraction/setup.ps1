# Quick Start Installation Script
# Run this script to set up the entire project

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "PDF to Excel Extraction - Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "ERROR: Python not found. Please install Python 3.9+ first." -ForegroundColor Red
    exit 1
}
$pythonVersion = python --version
Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    Write-Host "ERROR: Node.js not found. Please install Node.js 18+ first." -ForegroundColor Red
    exit 1
}
$nodeVersion = node --version
Write-Host "✓ Found Node.js: $nodeVersion" -ForegroundColor Green
Write-Host ""

# Backend Setup
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Backend Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

Set-Location backend

Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "Creating .env file..." -ForegroundColor Yellow
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "Please edit .env and add your OPENAI_API_KEY" -ForegroundColor Yellow
} else {
    Write-Host ".env already exists" -ForegroundColor Green
}

Set-Location ..
Write-Host ""

# Frontend Setup
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Frontend Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

Set-Location frontend

Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

Set-Location ..
Write-Host ""

# Summary
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit backend/.env and add your OPENAI_API_KEY" -ForegroundColor White
Write-Host "2. Install Tesseract OCR (see README.md)" -ForegroundColor White
Write-Host "3. Install Poppler for PDF conversion (see README.md)" -ForegroundColor White
Write-Host ""
Write-Host "To Run:" -ForegroundColor Yellow
Write-Host "Backend:  cd backend && python -m app.main" -ForegroundColor White
Write-Host "Frontend: cd frontend && npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Application:   http://localhost:5173" -ForegroundColor Green
