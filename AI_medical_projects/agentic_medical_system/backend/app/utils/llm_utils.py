from langchain_core.messages import BaseMessage, trim_messages
from langchain_core.language_models import BaseChatModel
from app.core.config import settings
from app.schemas.chat import Message

def dump_messages(messages: list[Message]) -> list[dict]:
    return [message.model_dump() for message in messages]

def prepare_messages(messages: list[Message], llm: BaseChatModel, system_prompt: str) -> list[Message]:
    """
    Trims messages to fit context window and prepends system prompt.
    """
    try:
        # Convert our pydantic messages to dicts for LangChain
        msg_dicts = dump_messages(messages)
        
        trimmed = trim_messages(
            msg_dicts,
            strategy="last",
            token_counter=llm,
            max_tokens=settings.MAX_TOKENS,
            start_on="human",
            include_system=False,
            allow_partial=False
        )
    except Exception:
        # Fallback
        trimmed = messages
        
    return [Message(role="system", content=system_prompt)] + trimmed # This might need adaptation if trimmed returns BaseMessages

def process_reasoning_blocks(content: str) -> str:
    """
    Helper to clean up reasoning blocks from some models if needed.
    """
    return content
