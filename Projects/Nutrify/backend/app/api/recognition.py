from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.ai_service import analyze_food_image
import json

router = APIRouter()

@router.post("/recognize")
async def recognize_food(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    contents = await file.read()
    result_text = await analyze_food_image(contents)
    
    if not result_text:
        raise HTTPException(status_code=500, detail="Failed to analyze image")
    
    # In a real scenario, we'd parse the JSON here.
    # For now, we return the raw text or try to parse it if the AI followed instructions perfectly.
    try:
        # Attempt to clean markdown code blocks if present
        cleaned_text = result_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned_text)
        return data
    except json.JSONDecodeError:
        return {"raw_response": result_text}
