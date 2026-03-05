# ContinuousCare - React.js + FastAPI

This project is a modernized version of the ContinuousCare website, built with React.js frontend and FastAPI backend.

## Project Structure

```
├── frontend/          # React.js application (Vite)
│   ├── public/        # Static assets
│   └── src/          # React components and pages
├── backend/           # FastAPI application
│   └── app/          # API routes and services
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- pip

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup

```bash
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Features

- **Frontend (React.js)**
  - Vite for fast development
  - React Router for navigation
  - TailwindCSS for styling
  - Responsive design
  - Component-based architecture

- **Backend (FastAPI)**
  - RESTful API
  - Contact form handling
  - CORS enabled for frontend communication
  - Auto-generated API documentation

## Development

### Frontend

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Backend

- `uvicorn app.main:app --reload` - Start development server with auto-reload
- API docs available at `/docs` and `/redoc`

## Original Design

This project maintains the exact UI/UX design from the original www.continuouscare.io website, including:
- Color scheme (teal/cyan theme)
- Typography (Inter font)
- Layout and components
- Responsive behavior

## Next Steps

1. Add more pages from the original site
2. Implement full contact form email functionality
3. Add blog functionality
4. Implement registration system
5. Add multi-language support

## License

All rights reserved - NeedStreet
