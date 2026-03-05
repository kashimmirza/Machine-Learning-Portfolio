from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.analysis import analysis_service
from app.core.limiter import limiter
from app.core.config import settings
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.post("/analyze")
@limiter.limit("5/minute")
async def analyze_image(
    request: Request,
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        content = await file.read()
        result = await analysis_service.analyze_medical_image(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import Request
