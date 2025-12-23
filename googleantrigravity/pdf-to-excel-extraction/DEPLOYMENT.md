# Deployment Guide

## Production Deployment

### Prerequisites

1. **Server Requirements**
   - Python 3.9+
   - Node.js 18+
   - 2GB+ RAM
   - 10GB+ disk space

2. **External Dependencies**
   - Tesseract OCR
   - Poppler utilities
   - OpenAI API account

### Option 1: Traditional Server Deployment

#### Backend Deployment

1. **Prepare environment:**
```bash
sudo apt-get update
sudo apt-get install python3-pip tesseract-ocr poppler-utils
```

2. **Clone and setup:**
```bash
git clone <repository-url>
cd pdf-to-excel-extraction/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
nano .env  # Add production values
```

4. **Run with systemd:**
Create `/etc/systemd/system/pdf-extraction-api.service`:
```ini
[Unit]
Description=PDF Extraction API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/pdf-extraction/backend
Environment="PATH=/var/www/pdf-extraction/backend/venv/bin"
ExecStart=/var/www/pdf-extraction/backend/venv/bin/python -m app.main
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable pdf-extraction-api
sudo systemctl start pdf-extraction-api
```

#### Frontend Deployment

1. **Build production bundle:**
```bash
cd frontend
npm install
npm run build
```

2. **Serve with Nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/pdf-extraction/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 2: Docker Deployment

TODO: Add Dockerfile and docker-compose.yml

### Option 3: Cloud Platform

#### AWS Deployment
- **Backend**: Elastic Beanstalk or ECS
- **Frontend**: S3 + CloudFront
- **Storage**: S3 for uploads/outputs
- **Database**: RDS for job persistence

#### Azure Deployment
- **Backend**: App Service or Container Instances
- **Frontend**: Static Web Apps or App Service
- **Storage**: Blob Storage
- **Database**: Azure SQL or Cosmos DB

#### Google Cloud
- **Backend**: Cloud Run or App Engine
- **Frontend**: Firebase Hosting or Cloud Storage
- **Storage**: Cloud Storage
- **Database**: Cloud SQL or Firestore

### Production Configuration

#### Backend (.env)
```env
DEBUG=False
LOG_LEVEL=WARNING
OPENAI_API_KEY=<your-production-key>
CORS_ORIGINS=https://your-domain.com
MAX_UPLOAD_SIZE_MB=100
```

#### Performance Tuning

1. **Backend:**
   - Use gunicorn with multiple workers
   - Enable response caching
   - Configure rate limiting
   - Set up log rotation

2. **Frontend:**
   - Enable CDN for static assets
   - Configure browser caching
   - Enable gzip compression
   - Optimize images

### Monitoring

#### Logs
```bash
# Backend logs
tail -f backend/logs/app.log
tail -f backend/logs/errors.log

# Systemd logs
journalctl -u pdf-extraction-api -f
```

#### Health Checks
- API: `GET http://your-domain/health`
- Frontend: Check 200 status on root

### Security

1. **API Security:**
   - Add API key authentication
   - Enable HTTPS only
   - Set up CORS properly
   - Rate limit endpoints

2. **File Security:**
   - Validate file types
   - Scan for malware
   - Set file size limits
   - Automatic cleanup of old files

3. **Environment:**
   - Use environment variables
   - Never commit .env files
   - Rotate API keys regularly
   - Use secrets management

### Backup

1. **Data:**
   - Backup outputs directory daily
   - Store logs for 30 days
   - Keep database backups

2. **Code:**
   - Version control with Git
   - Tag releases
   - Document changes

### Scaling

#### Horizontal Scaling
- Deploy multiple backend instances
- Use load balancer
- Share storage (S3/Azure Blob)
- Add Redis for job state

#### Vertical Scaling
- Increase server resources
- Optimize database queries
- Add caching layer
- Use async processing

### Cost Optimization

1. **OpenAI API:**
   - Use Tesseract for simple documents
   - Implement caching
   - Set usage limits
   - Monitor API costs

2. **Infrastructure:**
   - Auto-scaling
   - Reserved instances
   - Serverless where possible
   - Storage lifecycle policies

### Maintenance

#### Regular Tasks
- Update dependencies monthly
- Review logs weekly
- Clean old files daily
- Monitor API usage

#### Updates
```bash
git pull
cd backend && pip install -r requirements.txt
cd frontend && npm install && npm run build
sudo systemctl restart pdf-extraction-api
```

## Troubleshooting

### Common Issues

1. **Tesseract not found:**
```bash
# Linux
sudo apt-get install tesseract-ocr

# Add to PATH
export PATH="/usr/share/tesseract-ocr:$PATH"
```

2. **Poppler not found:**
```bash
# Linux
sudo apt-get install poppler-utils
```

3. **Port already in use:**
```bash
# Change port in app/main.py
uvicorn.run(..., port=8001)
```

4. **CORS errors:**
- Add frontend URL to CORS_ORIGINS in .env
- Check backend logs for details

### Support Contacts

- Technical Issues: [support email]
- API Questions: [api support]
- Billing: [billing contact]
