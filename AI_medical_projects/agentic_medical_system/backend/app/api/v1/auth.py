from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.auth import UserCreate, UserResponse, Token
from app.services.database import database_service
from app.models.user import User
from app.utils.auth import create_access_token, verify_token
from app.utils.sanitization import sanitize_email
from app.core.limiter import limiter
from fastapi import Request
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await database_service.get_user(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/register", response_model=UserResponse)
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["auth"][0])
async def register(request: Request, user_data: UserCreate):
    email = sanitize_email(user_data.email)
    existing_user = await database_service.get_user_by_email(email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = User.get_password_hash(user_data.password)
    user = await database_service.create_user(email, hashed_password)
    
    token = create_access_token(str(user.id))
    return UserResponse(id=user.id, email=user.email, token=token)

@router.post("/login", response_model=UserResponse)
@limiter.limit(settings.RATE_LIMIT_ENDPOINTS["auth"][0])
async def login(request: Request, user_data: UserCreate):
    email = sanitize_email(user_data.email)
    user = await database_service.get_user_by_email(email)
    if not user or not User.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(str(user.id))
    return UserResponse(id=user.id, email=user.email, token=token)
