from typing import List, Any, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import RateLimitError, APITimeoutError, APIError

from app.core.config import settings
from app.core.logging import logger

class LLMRegistry:
    LLMS: List[Dict[str, Any]] = [
        {
            "name": "gpt-4-turbo", 
            "llm": ChatOpenAI(
                model=settings.DEFAULT_LLM_MODEL,
                api_key=settings.OPENAI_API_KEY,
                temperature=settings.DEFAULT_LLM_TEMPERATURE
            )
        },
        {
            "name": "gpt-3.5-turbo",
            "llm": ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=settings.OPENAI_API_KEY,
                temperature=settings.DEFAULT_LLM_TEMPERATURE
            )
        }
    ]
    
    @classmethod
    def get(cls, name: str):
        for entry in cls.LLMS:
            if entry["name"] == name:
                return entry["llm"]
        return cls.LLMS[0]["llm"]

class LLMService:
    def __init__(self):
        self._llm = LLMRegistry.get(settings.DEFAULT_LLM_MODEL)
        
    def get_llm(self):
        return self._llm

    @retry(
        stop=stop_after_attempt(settings.MAX_LLM_CALL_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError)),
        reraise=True
    )
    async def call(self, messages: List[Dict]) -> BaseMessage:
        if not self._llm:
            raise RuntimeError("LLM not initialized")
        return await self._llm.ainvoke(messages)
    
    def bind_tools(self, tools: List[Any]):
        if self._llm:
            self._llm = self._llm.bind_tools(tools)
        return self

llm_service = LLMService()
