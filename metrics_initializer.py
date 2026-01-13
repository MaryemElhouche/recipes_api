from prometheus_client import Gauge, REGISTRY
import random
import time
from contextlib import asynccontextmanager

def get_or_create_gauge(name, description, labelnames=None):
    """Get existing gauge or create new one to avoid duplicate registration"""
    labelnames = labelnames or []
    
    # First, try to find if it already exists
    for collector in list(REGISTRY._collector_to_names.keys()):
        if hasattr(collector, '_name') and collector._name == name:
            print(f"ℹ️ Metric '{name}' already exists, reusing it")
            return collector
    
    # If not found, create it
    try:
        metric = Gauge(name, description, labelnames)
        print(f"✅ Created new metric '{name}'")
        return metric
    except ValueError as e:
        # If creation fails, try to find it again (race condition)
        print(f"⚠️ Error creating metric '{name}': {e}")
        for collector in list(REGISTRY._collector_to_names.keys()):
            if hasattr(collector, '_name') and collector._name == name:
                print(f"ℹ️ Found existing metric '{name}' after error")
                return collector
        print(f"❌ Could not create or find metric '{name}'")
        return None

# Only create if it doesn't exist
REQUEST_COUNT_CREATED = get_or_create_gauge(
    'request_count_created',
    'Timestamp of request',
    ['endpoint', 'http_status', 'method']
)

# Endpoints configuration
endpoints = ["/", "/recipes", "/crash", "/metrics"]
methods = ["GET", "POST", "PUT", "DELETE"]
statuses = ["200", "404", "500"]

def initialize_static_metrics():
    """Initialize Prometheus metrics with test data"""
    try:
        print("🚀 Initializing Prometheus metrics...")
        
        # Import here to avoid circular dependency
        from main import REQUEST_COUNT, ERROR_COUNT, REQUEST_LATENCY
        
        for ep in endpoints:
            for method in methods:
                for status in statuses:
                    # Generate realistic volumes
                    if ep == "/":
                        volume = random.randint(100, 300)
                    elif ep == "/recipes":
                        volume = random.randint(50, 200)
                    else:
                        volume = random.randint(5, 30)
                    
                    REQUEST_COUNT.labels(method, ep, status).inc(volume)
                    
                    # Add latency observations
                    for _ in range(10):
                        if status == "500":
                            latency = random.uniform(2.0, 5.0)
                        elif status == "200":
                            latency = random.uniform(0.05, 0.5)
                        else:
                            latency = random.uniform(0.1, 1.0)
                        REQUEST_LATENCY.labels(ep).observe(latency)
                    
                    # Set timestamps only if metric exists
                    if REQUEST_COUNT_CREATED is not None:
                        try:
                            REQUEST_COUNT_CREATED.labels(ep, status, method).set(time.time())
                        except Exception as e:
                            print(f"⚠️ Could not set timestamp for {ep}: {e}")
            
            # Add error counts
            ERROR_COUNT.labels(ep).inc(random.randint(1, 10))
        
        print("✅ Metrics initialized successfully!")
        
    except Exception as e:
        print(f"⚠️ Error during metrics initialization: {e}")
        import traceback
        traceback.print_exc()

@asynccontextmanager
async def lifespan(app_instance):
    """FastAPI lifespan handler for startup/shutdown"""
    # STARTUP
    print("🚀 Application starting...")
    initialize_static_metrics()
    print("📈 Metrics available at http://localhost:8000/metrics")
    
    yield  # Application runs
    
    # SHUTDOWN
    print("👋 Application shutting down...")