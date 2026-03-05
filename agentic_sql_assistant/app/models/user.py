from typing import List, Optional
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

class User(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    
    sessions: List["Session"] = Relationship(back_populates="user")
