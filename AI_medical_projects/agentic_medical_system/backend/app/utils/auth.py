from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from app.core.config import settings
from app.schemas.auth import Token
from app.utils.sanitization import sanitize_string

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> Token:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_ACCESS_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "jti": sanitize_string(f"{subject}-{datetime.now(timezone.utc).timestamp()}"),
    }
    
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer", expires_at=expire)

def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
