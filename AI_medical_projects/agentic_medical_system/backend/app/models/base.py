from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel

class BaseModel(SQLModel):
    """
    Abstract base model that adds common fields to all tables.
    """
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
