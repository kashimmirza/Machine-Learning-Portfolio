from typing import Optional, List
from sqlmodel import Field, Relationship
from app.models.base import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class Session(BaseModel, table=True):
    id: str = Field(primary_key=True) # UUID
    name: Optional[str] = None
    user_id: int = Field(foreign_key="user.id")
    
    user: "User" = Relationship(back_populates="sessions")
