<!-- @format -->

# 🔒 SECURITY GUIDE - API Key Management

## ⚠️ CRITICAL SECURITY ISSUE DETECTED

Your API keys were exposed in the conversation. **Take immediate action:**

### 1. Rotate OpenAI API Key (URGENT)

```bash
# Go to: https://platform.openai.com/api-keys
# 1. Click on the exposed key
# 2. Click "Revoke" or "Delete"
# 3. Create new key
# 4. Update your .env file
```

### 2. Rotate Pinecone API Key (URGENT)

```bash
# Go to: https://app.pinecone.io/
# 1. Navigate to API Keys
# 2. Delete the exposed key
# 3. Generate new key
# 4. Update your .env file
```

### 3. Security Best Practices

#### ✅ DO:

1. **Use .env files** for local development
2. **Add .env to .gitignore**
3. **Use environment variables** in production
4. **Use secret managers** (AWS Secrets Manager, Azure Key Vault)
5. **Rotate keys regularly** (every 90 days)
6. **Use different keys** for dev/staging/prod
7. **Monitor API usage** for anomalies
8. **Set spending limits** on OpenAI account

#### ❌ DON'T:

1. **Never commit .env** to version control
2. **Never share keys** in chat/email/slack
3. **Never hardcode keys** in code
4. **Never use production keys** in development
5. **Never expose keys** in client-side code
6. **Never screenshot keys**
7. **Never post keys** online (forums, stackoverflow)

## Secure Setup Guide

### Step 1: Create .gitignore

```bash
# Create .gitignore in project root
cat > .gitignore << 'EOF'
# Environment files
.env
.env.local
.env.*.local
*.env

# API Keys
*api_key*
*secret*

# Credentials
credentials.json
service-account.json

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite
*.sqlite3

# Pinecone
pinecone_index/
checkpoints.db

# Temporary
tmp/
temp/
*.tmp
EOF
```

### Step 2: Create Secure .env File

```bash
# Copy example to .env
cp backend/.env.example backend/.env

# Edit with your NEW keys
nano backend/.env

# Set restrictive permissions
chmod 600 backend/.env
```

### Step 3: Verify .env is Ignored

```bash
git status

# Should NOT see .env file
# If you see it:
git rm --cached backend/.env
git commit -m "Remove .env from tracking"
```

## Environment-Specific Configuration

### Development (.env)

```env
ENVIRONMENT=development
OPENAI_API_KEY=sk-proj-dev-...
PINECONE_API_KEY=pcsk-dev-...
DEBUG=true
```

### Staging (.env.staging)

```env
ENVIRONMENT=staging
OPENAI_API_KEY=sk-proj-staging-...
PINECONE_API_KEY=pcsk-staging-...
DEBUG=false
```

### Production (Environment Variables)

```bash
# Set via CI/CD or server
export OPENAI_API_KEY="sk-proj-prod-..."
export PINECONE_API_KEY="pcsk-prod-..."
export ENVIRONMENT="production"
```

## Using Secret Managers

### AWS Secrets Manager

```python
# backend/config/secrets.py
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name: str) -> dict:
    """Get secret from AWS Secrets Manager"""
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        raise e

# Usage
secrets = get_secret("prod/multimodal-search")
OPENAI_API_KEY = secrets['openai_api_key']
PINECONE_API_KEY = secrets['pinecone_api_key']
```

### Azure Key Vault

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_azure_secret(secret_name: str) -> str:
    """Get secret from Azure Key Vault"""
    vault_url = "https://your-vault.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    return client.get_secret(secret_name).value

# Usage
OPENAI_API_KEY = get_azure_secret("openai-api-key")
```

### Google Cloud Secret Manager

```python
from google.cloud import secretmanager

def get_gcp_secret(project_id: str, secret_id: str) -> str:
    """Get secret from GCP Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Usage
OPENAI_API_KEY = get_gcp_secret("my-project", "openai-api-key")
```

## Docker Secrets

### docker-compose.yml

```yaml
version: "3.8"

services:
 backend:
  build: ./backend
  environment:
   - OPENAI_API_KEY_FILE=/run/secrets/openai_key
   - PINECONE_API_KEY_FILE=/run/secrets/pinecone_key
  secrets:
   - openai_key
   - pinecone_key

secrets:
 openai_key:
  external: true
 pinecone_key:
  external: true
```

### Create Docker Secrets

```bash
# Create secrets
echo "sk-proj-your-key" | docker secret create openai_key -
echo "pcsk-your-key" | docker secret create pinecone_key -

# Use in code
with open('/run/secrets/openai_key', 'r') as f:
    OPENAI_API_KEY = f.read().strip()
```

## Monitoring & Alerts

### 1. Set Up OpenAI Usage Alerts

```python
# Monitor OpenAI usage
from openai import OpenAI

client = OpenAI()

# Check usage
usage = client.usage.list(date="2024-01-01")
print(f"Total tokens: {usage.total_tokens}")
print(f"Cost: ${usage.total_cost}")

# Set up alerts if cost > threshold
if usage.total_cost > 100:
    send_alert("OpenAI costs exceeding budget!")
```

### 2. Monitor API Key Usage

```python
# Log all API calls
import logging

logger = logging.getLogger(__name__)

def make_api_call():
    logger.info(f"API call made by user: {user_id}")
    logger.info(f"Endpoint: {endpoint}")
    logger.info(f"Timestamp: {timestamp}")
```

### 3. Set Up Rate Limiting

```python
from fastapi import HTTPException
from collections import defaultdict
import time

# Rate limiter
class RateLimiter:
    def __init__(self, calls_per_minute=60):
        self.calls = defaultdict(list)
        self.limit = calls_per_minute

    def check_rate_limit(self, api_key: str) -> bool:
        now = time.time()

        # Remove old calls
        self.calls[api_key] = [
            t for t in self.calls[api_key]
            if now - t < 60
        ]

        # Check limit
        if len(self.calls[api_key]) >= self.limit:
            raise HTTPException(429, "Rate limit exceeded")

        self.calls[api_key].append(now)
        return True
```

## Key Rotation Procedure

### Automated Rotation (Recommended)

```python
# backend/scripts/rotate_keys.py
import os
from datetime import datetime, timedelta

def should_rotate_key(key_age_days: int) -> bool:
    """Check if key should be rotated"""
    return key_age_days > 90  # Rotate every 90 days

def rotate_openai_key():
    """Rotate OpenAI API key"""
    # 1. Generate new key via OpenAI API
    # 2. Update secret manager
    # 3. Update applications
    # 4. Revoke old key after grace period
    pass

# Run via cron job
if __name__ == "__main__":
    rotate_openai_key()
```

## Emergency Response

### If Key is Exposed:

1. **Immediate Actions** (within 5 minutes):

   ```bash
   # Revoke key immediately
   # Generate new key
   # Update all services
   ```

2. **Investigation** (within 1 hour):

   ```bash
   # Check API usage logs
   # Identify unauthorized usage
   # Document incident
   ```

3. **Prevention** (within 24 hours):
   ```bash
   # Implement secret scanning
   # Update security policies
   # Train team members
   ```

## Secret Scanning

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check for potential secrets
if git diff --cached | grep -i "api_key\|secret\|password" | grep -v ".env.example"; then
    echo "❌ Potential secret detected!"
    echo "Please remove secrets before committing"
    exit 1
fi
```

### GitHub Secret Scanning

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
 scan:
  runs-on: ubuntu-latest
  steps:
   - uses: actions/checkout@v2

   - name: Run secret scan
     uses: trufflesecurity/trufflehog@main
     with:
      path: ./
      base: ${{ github.event.repository.default_branch }}
```

## Configuration Manager

```python
# backend/config/settings.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    # Pinecone
    pinecone_api_key: str
    pinecone_index: str = "multimodal-search-index"

    # Environment
    environment: str = "development"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Usage
settings = Settings()

# Keys are never exposed in code
client = OpenAI(api_key=settings.openai_api_key)
```

## Checklist

Before deploying to production:

- [ ] All .env files in .gitignore
- [ ] No hardcoded keys in code
- [ ] Using secret manager (AWS/Azure/GCP)
- [ ] Different keys for dev/staging/prod
- [ ] API usage monitoring enabled
- [ ] Rate limiting implemented
- [ ] Spending limits set
- [ ] Key rotation schedule established
- [ ] Team trained on security practices
- [ ] Incident response plan documented

## Resources

- OpenAI Security: https://platform.openai.com/docs/guides/safety-best-practices
- Pinecone Security: https://docs.pinecone.io/docs/security
- OWASP API Security: https://owasp.org/www-project-api-security/
- Secret Management: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

---

**Remember: Security is not optional. Protect your keys like you protect your passwords!** 🔒
