from prometheus_client import Counter, Histogram, Gauge
from starlette_prometheus import metrics, PrometheusMiddleware

# 1. Standard HTTP Metrics
http_requests_total = Counter(
    "http_requests_total", 
    "Total number of HTTP requests", 
    ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds", 
    "HTTP request duration in seconds", 
    ["method", "endpoint"]
)

# 2. Infrastructure Metrics
db_connections = Gauge(
    "db_connections", 
    "Number of active database connections"
)

# 3. AI / Business Logic Metrics
llm_inference_duration_seconds = Histogram(
    "llm_inference_duration_seconds",
    "Time spent processing LLM inference",
    ["model"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0] 
)

def setup_metrics(app):
    """
    Configures the Prometheus middleware and exposes the /metrics endpoint.
    """
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", metrics)
