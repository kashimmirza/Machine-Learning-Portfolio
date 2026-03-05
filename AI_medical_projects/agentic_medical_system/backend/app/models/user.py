from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from passlib.context import CryptContext
from .base import BaseModel

if TYPE_CHECKING:
    from .session import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

    sessions: List["Session"] = Relationship(back_populates="user")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
