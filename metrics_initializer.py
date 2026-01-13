from prometheus_client import Gauge, REGISTRY
import random
import time
import asyncio
from contextlib import asynccontextmanager

def get_or_create_gauge(name, description, labelnames=None):
    """Get existing gauge or create new one to avoid duplicate registration"""
    labelnames = labelnames or []
    
    # Check if metric already exists in registry
    for collector in list(REGISTRY._collector_to_names.keys()):
        if hasattr(collector, '_name') and collector._name == name:
            print(f"ℹ️ Metric '{name}' already exists, reusing it")
            return collector
    
    # Create new metric if it doesn't exist
    try:
        return Gauge(name, description, labelnames)
    except ValueError as e:
        print(f"⚠️ Error creating metric '{name}': {e}")
        return None

# Gauge pour horodatage - FIXED to avoid duplicates
REQUEST_COUNT_CREATED = get_or_create_gauge(
    'request_count_created',
    'Timestamp of request',
    ['endpoint', 'http_status', 'method']
)

# Endpoints / méthodes / statuts à simuler (matching your actual endpoints)
endpoints = ["/", "/recipes", "/crash", "/metrics"]
methods = ["GET", "POST", "PUT", "DELETE"]
statuses = ["200", "404", "500"]

def initialize_static_metrics():
    """Pré-remplit toutes les séries Prometheus pour tests"""
    try:
        print("🚀 Initialisation des métriques Prometheus...")
        
        # Import here to avoid circular dependency
        from main import REQUEST_COUNT, ERROR_COUNT, REQUEST_LATENCY
        
        for ep in endpoints:
            for method in methods:
                for status in statuses:
                    # Générer des volumes réalistes
                    if ep == "/":
                        volume = random.randint(100, 300)
                    elif ep == "/recipes":
                        volume = random.randint(50, 200)
                    else:
                        volume = random.randint(5, 30)
                    
                    REQUEST_COUNT.labels(method, ep, status).inc(volume)
                    
                    # Latences variées
                    for _ in range(10):
                        if status == "500":
                            latency = random.uniform(2.0, 5.0)
                        elif status == "200":
                            latency = random.uniform(0.05, 0.5)
                        else:
                            latency = random.uniform(0.1, 1.0)
                        REQUEST_LATENCY.labels(ep).observe(latency)
                    
                    # Timestamps
                    if REQUEST_COUNT_CREATED is not None:
                        REQUEST_COUNT_CREATED.labels(ep, status, method).set(time.time())
            
            # Force error_count_total à 1 pour chaque endpoint
            ERROR_COUNT.labels(ep).inc(random.randint(1, 10))
        
        print("✅ Métriques statiques initialisées avec succès!")
        
    except Exception as e:
        print(f"⚠️ Erreur lors de l'initialisation des métriques: {e}")

async def generate_continuous_metrics():
    """Génère continuellement des métriques réalistes"""
    print("🔄 Génération continue de métriques activée...")
    
    # Import here to avoid circular dependency
    from main import REQUEST_COUNT, ERROR_COUNT, REQUEST_LATENCY
    
    while True:
        try:
            # Simuler 5-10 requêtes par cycle
            for _ in range(random.randint(5, 10)):
                ep = random.choice(endpoints)
                method = random.choice(methods)
                
                # Distribution réaliste des statuts (85% succès)
                if random.random() < 0.85:
                    status = "200"
                elif random.random() < 0.90:
                    status = "404"
                else:
                    status = "500"
                
                REQUEST_COUNT.labels(method, ep, status).inc(1)
                
                # Latence réaliste
                if status == "500":
                    latency = random.uniform(1.5, 4.0)
                    ERROR_COUNT.labels(ep).inc(1)
                else:
                    latency = random.uniform(0.05, 0.3)
                
                REQUEST_LATENCY.labels(ep).observe(latency)
                
                if REQUEST_COUNT_CREATED is not None:
                    REQUEST_COUNT_CREATED.labels(ep, status, method).set(time.time())
            
            await asyncio.sleep(3)
            
        except Exception as e:
            print(f"⚠️ Erreur dans la génération continue: {e}")
            await asyncio.sleep(5)

@asynccontextmanager
async def lifespan(app_instance):
    """Lifecycle manager for FastAPI startup and shutdown events"""
    # STARTUP: Initialize metrics when app starts
    print("🚀 Starting application...")
    initialize_static_metrics()
    
    # Optional: Start continuous metrics generation
    # Uncomment the line below if you want continuous metric generation
    # asyncio.create_task(generate_continuous_metrics())
    
    print("✅ Système de métriques Prometheus complètement initialisé!")
    print("📈 Métriques disponibles sur http://localhost:8000/metrics")
    
    yield  # Application runs here
    
    # SHUTDOWN: Cleanup when app stops
    print("👋 Shutting down application...")