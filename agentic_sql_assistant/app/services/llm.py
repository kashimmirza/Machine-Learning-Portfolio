from typing import Any, Dict, List, Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from openai import APIError, APITimeoutError, OpenAIError, RateLimitError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
import logging

from app.core.config import settings

# Setup simple logger
logger = logging.getLogger("agent")

# ==================================================
# LLM Registry
# ==================================================
class LLMRegistry:
    """
    Registry of available LLM models.
    This allows us to switch "Brains" on the fly without changing code.
    """
    
    # We pre-configure models with different capabilities/costs
    # Note: In a real Scenario, we would instantiate these lazily or via config
    LLMS: List[Dict[str, Any]] = []

    @classmethod
    def initialize(cls):
        # Primary: Azure OpenAI (if configured) or GPT-4
        if settings.AZURE_OPENAI_ENDPOINT:
            primary = AzureChatOpenAI(
                azure_deployment=settings.AZURE_DEPLOYMENT_NAME,
                openai_api_version=settings.AZURE_OPENAI_API_VERSION,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_key=settings.OPENAI_API_KEY,
                temperature=0,
                max_tokens=settings.MAX_TOKENS,
            )
        else:
            primary = ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                temperature=0,
                max_tokens=settings.MAX_TOKENS,
                model="gpt-4" 
            )
            
        # Fallback: Standard OpenAI (cheaper/backup)
        # For this MVP, we just reuse the same logic but maybe a different model param if we had it
        fallback = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            temperature=0,
            max_tokens=settings.MAX_TOKENS,
            model="gpt-3.5-turbo" # Explicit fallback 
        )

        cls.LLMS = [
            {"name": "primary", "llm": primary},
            {"name": "fallback", "llm": fallback},
        ]

    @classmethod
    def get(cls, model_name: str) -> BaseChatModel:
        """Retrieve a specific model instance by name."""
        if not cls.LLMS:
             cls.initialize()
             
        for entry in cls.LLMS:
            if entry["name"] == model_name:
                return entry["llm"]
        # Default to first if not found
        return cls.LLMS[0]["llm"]
    
    @classmethod
    def get_all_names(cls) -> List[str]:
        if not cls.LLMS:
             cls.initialize()
        return [entry["name"] for entry in cls.LLMS]

# ==================================================
# LLM Service (The Resilience Layer)
# ==================================================

class LLMService:
    """
    Manages LLM calls with automatic retries and fallback logic.
    """

    def __init__(self):
        self._llm: Optional[BaseChatModel] = None
        self._current_model_index: int = 0
        LLMRegistry.initialize()
        
        # Initialize with the primary model
        try:
            self._llm = LLMRegistry.LLMS[0]["llm"]
            self._current_model_index = 0
        except Exception:
            # Fallback safety
            pass

    def _switch_to_next_model(self) -> bool:
        """
        Circular Fallback: Switches to the next available model in the registry.
        Returns True if successful.
        """
        try:
            next_index = (self._current_model_index + 1) % len(LLMRegistry.LLMS)
            next_model_entry = LLMRegistry.LLMS[next_index]
            
            logger.warning(
                f"switching_model_fallback old_index={self._current_model_index} new_model={next_model_entry['name']}"
            )
            self._current_model_index = next_index
            self._llm = next_model_entry["llm"]
            return True
        except Exception as e:
            logger.error(f"model_switch_failed error={str(e)}")
            return False

    # --------------------------------------------------
    # The Retry Decorator
    # --------------------------------------------------
    @retry(
        stop=stop_after_attempt(3), # Stop after 3 tries
        wait=wait_exponential(multiplier=1, min=2, max=10),     # Wait 2s, 4s, 8s...
        retry=retry_if_exception_type((RateLimitError, APITimeoutError, APIError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),       # Log before waiting
        reraise=True,
    )
    async def _call_with_retry(self, messages: List[BaseMessage]) -> BaseMessage:
        """Internal method that executes the actual API call."""
        if not self._llm:
            raise RuntimeError("LLM not initialized")
        return await self._llm.ainvoke(messages)

    async def call(self, messages: List[BaseMessage]) -> BaseMessage:
        """
        Public interface. Wraps the retry logic with a Fallback loop.
        """
        total_models = len(LLMRegistry.LLMS)
        models_tried = 0
        
        while models_tried < total_models:
            try:
                # Attempt to generate response
                return await self._call_with_retry(messages)
            
            except OpenAIError as e:
                # If we exhausted retries for THIS model, log and switch
                models_tried += 1
                logger.error(
                    f"model_failed_exhausted_retries model={LLMRegistry.LLMS[self._current_model_index]['name']} error={str(e)}"
                )
                
                if models_tried >= total_models:
                    break
                
                self._switch_to_next_model()
        raise RuntimeError("Failed to get response from any LLM after exhausting all options.")

    def get_llm(self) -> BaseChatModel:
        return self._llm
    
    def bind_tools(self, tools: List[Any]):
        """Bind tools to the current LLM instance."""
        if self._llm:
            self._llm = self._llm.bind_tools(tools)
            # We also need to update the registry instances to have tools bound? 
            # In a real app this is complex because binding creates a NEW object.
            # For simplicity in this MVP, we just update the current pointer.
        return self

llm_service = LLMService()
