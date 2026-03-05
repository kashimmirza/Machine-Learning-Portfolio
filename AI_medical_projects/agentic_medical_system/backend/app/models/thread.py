from sqlmodel import Field, SQLModel
from datetime import datetime, timezone

class Thread(SQLModel, table=True):
    """
    Acts as a lightweight anchor for LangGraph checkpoints.
    """
    id: str = Field(primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
