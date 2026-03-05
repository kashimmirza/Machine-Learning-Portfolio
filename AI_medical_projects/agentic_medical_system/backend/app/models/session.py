from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from .base import BaseModel

if TYPE_CHECKING:
    from .user import User

class Session(BaseModel, table=True):
    id: str = Field(primary_key=True) # UUID
    user_id: int = Field(foreign_key="user.id")
    name: Optional[str] = Field(default=None)

    user: "User" = Relationship(back_populates="sessions")
