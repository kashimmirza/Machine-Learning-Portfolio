from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(min_length=1)

class ChatRequest(BaseModel):
    messages: List[Message]
    # Optional: Image data for medical analysis could theoretically be sent here as base64 or separate upload
    image_url: Optional[str] = None

class ChatResponse(BaseModel):
    messages: List[Message]

class StreamResponse(BaseModel):
    content: str = ""
    done: bool = False
