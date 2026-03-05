from contextvars import ContextVar
from typing import Optional, Dict, Any
import structlog
import logging
import sys

# Context variable to hold request-scoped metadata
_context: ContextVar[Dict[str, Any]] = ContextVar("context", default={})

def bind_context(**kwargs):
    """
    Bind metadata to the current request context.
    """
    ctx = _context.get()
    ctx.update(kwargs)
    _context.set(ctx)

def clear_context():
    """
    Clear the current request context using a new empty dict.
    """
    _context.set({})

def get_context() -> Dict[str, Any]:
    return _context.get()

# Processor to inject context into structlog
def context_processor(logger, log_method, event_dict):
    ctx = get_context()
    event_dict.update(ctx)
    return event_dict

# Configure structlog
structlog.configure(
    processors=[
        context_processor,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()
