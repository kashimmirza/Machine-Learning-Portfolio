from prometheus_client import Counter, Histogram, Gauge
from starlette_prometheus import metrics, PrometheusMiddleware

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

def setup_metrics(app):
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", metrics)
