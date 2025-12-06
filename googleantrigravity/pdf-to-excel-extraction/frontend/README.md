# Frontend - PDF Extraction UI

React + Vite frontend for the PDF to Excel extraction application.

## Features

- Drag-and-drop file upload
- Real-time processing status
- Interactive results viewer
- Responsive design
- Dark theme with premium styling

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

4. Preview production build:
```bash
npm run preview
```

## Components

### FileUploader
Drag-and-drop file upload with preview and file management.

### ProcessingStatus
Real-time job status with progress bar and live updates.

### ResultsViewer
Display extracted data with download options.

## API Integration

The frontend communicates with the backend API through the `api.js` service.

API base URL is configured via:
- Environment variable: `VITE_API_URL`
- Default: `http://localhost:8000`

During development, Vite proxy is used for API calls.

## Styling

Built with vanilla CSS featuring:
- Modern dark theme
- Smooth animations
- Responsive design
- Premium gradients and shadows

## Environment Variables

Create `.env.local` for custom configuration:

```
VITE_API_URL=http://localhost:8000
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
