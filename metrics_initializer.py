from prometheus_client import Gauge
import random
import time
from main import app, REQUEST_COUNT, ERROR_COUNT, REQUEST_LATENCY

# Gauge pour horodatage
REQUEST_COUNT_CREATED = Gauge(
    'request_count_created',
    'Timestamp of request',
    ['endpoint', 'http_status', 'method']
)

# Endpoints / méthodes / statuts à simuler
endpoints = ["/", "/recipes", "/favicon.ico", "/metrics", "/sitemap.xml", "/robots.txt"]
methods = ["GET", "POST"]
statuses = ["200", "404", "500"]

@app.on_event("startup")
def initialize_metrics():
    """Pré-remplit toutes les séries Prometheus pour tests, et force error_count_total à 1 sur chaque endpoint."""
    for ep in endpoints:
        for method in methods:
            for status in statuses:
                # Counter existants
                REQUEST_COUNT.labels(method, ep, status).inc(random.randint(0, 5))
                REQUEST_LATENCY.labels(ep).observe(random.random())  # latence aléatoire 0-1s
                REQUEST_COUNT_CREATED.labels(ep, status, method).set(time.time())
        # Force error_count_total à 1 pour chaque endpoint
        ERROR_COUNT.labels(ep).inc(1)
    print("✅ Métriques initialisées au démarrage (error_count_total forcé à 1 sur chaque endpoint) !")
