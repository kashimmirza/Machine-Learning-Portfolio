import time
from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.metrics import (
    http_request_duration_seconds,
    http_requests_total,
)

# ==================================================
# Metrics Middleware
# ==================================================
class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to automatically track request duration and status codes.
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        try:
            # Process the actual request
            response = await call_next(request)
            status_code = response.status_code
            return response
            
        except Exception:
            # If the app crashes, we still want to record the 500 error
            status_code = 500
            raise
            
        finally:
            # Calculate duration even if it failed
            duration = time.time() - start_time
            
            # Record to Prometheus
            if request.url.path not in ["/metrics", "/health", "/openapi.json"]:
                http_requests_total.labels(
                    method=request.method, 
                    endpoint=request.url.path, 
                    status=status_code
                ).inc()
                
                http_request_duration_seconds.labels(
                    method=request.method, 
                    endpoint=request.url.path
                ).observe(duration)
