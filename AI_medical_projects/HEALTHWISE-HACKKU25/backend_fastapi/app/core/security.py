from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import jwt
from app.core.config import settings

# Node usually sends 'token' in headers or 'Authorization: Bearer <token>'
# Based on middleware/authDoctor.js, it looks like 'dtoken' or similar. 
# We'll support standard Bearer token for cleanliness, or 'token' header.
# Adjusting to standard Bearer for Agentic API, but capable of verifying shared secret.

oauth2_scheme = APIKeyHeader(name="Authorization", auto_error=False) 

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        # Allow open access for now for testing, OR implement strict checking
        # raise HTTPException(status_code=401, detail="Missing Token")
        return None # Return None if no token, let endpoint decide

    try:
        # Standardize: Remove 'Bearer ' if present
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
            
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
