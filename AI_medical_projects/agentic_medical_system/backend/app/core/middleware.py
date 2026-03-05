import time
from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.metrics import http_requests_total, http_request_duration_seconds
from app.core.logging import bind_context, clear_context, logger

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        status_code = 500
        
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration = time.time() - start_time
            if request.url.path not in ["/metrics", "/health"]:
                http_requests_total.labels(
                    method=request.method,
                    endpoint=request.url.path,
                    status=status_code
                ).inc()
                http_request_duration_seconds.labels(
                    method=request.method,
                    endpoint=request.url.path
                ).observe(duration)

class LoggingContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        clear_context()
        try:
            # We could try to extract user_id from token here for logs if needed
            # For now, just basic request info
            bind_context(path=request.url.path, method=request.method)
            response = await call_next(request)
            return response
        finally:
            clear_context()
