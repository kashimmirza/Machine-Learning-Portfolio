from abc import ABC, abstractmethod
from typing import Any, Dict
from app.core.logging import logger

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """Process the input data and return a result."""
        pass

    def log_thought(self, thought: str):
        logger.info(f"[{self.name}] {thought}")
