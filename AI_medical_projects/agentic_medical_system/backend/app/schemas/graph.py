from typing import Annotated, Any
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class GraphState(BaseModel):
    """
    State object passed between graph nodes.
    """
    messages: Annotated[list, add_messages] = Field(default_factory=list)
    long_term_memory: str = Field(default="")
    user_id: str = Field(default="")
