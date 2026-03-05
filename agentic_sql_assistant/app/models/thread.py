from sqlmodel import Field
from app.models.base import BaseModel

class Thread(BaseModel, table=True):
    id: str = Field(primary_key=True)
    # LangGraph state is stored separately by the checkpointer, 
    # but we keep this for referential integrity if needed.
