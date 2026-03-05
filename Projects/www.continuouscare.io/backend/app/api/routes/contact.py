from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str
    phone: Optional[str] = None

@router.post("/contact")
async def submit_contact_form(contact: ContactMessage):
    """
    Handle contact form submissions
    TODO: Implement email sending logic
    """
    try:
        # For now, just log the message
        # In production, you would send an email here
        print(f"Contact form submitted: {contact.name} - {contact.email}")
        
        return {
            "success": True,
            "message": "Thank you for contacting us. We'll get back to you soon!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
