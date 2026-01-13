import json
import uuid
import time

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from typing import List
from loguru import logger
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Prometheus metrics (declare BEFORE importing metrics_initializer)
REQUEST_COUNT = Counter('request_count', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'HTTP request latency', ['endpoint'])
ERROR_COUNT = Counter('error_count', 'Total errors', ['endpoint'])

# Import lifespan AFTER declaring metrics
from metrics_initializer import lifespan

# --- Création de l'app FastAPI avec lifespan ---
app = FastAPI(title="API Recettes Cuisine", lifespan=lifespan)

# --- Endpoint de test pour générer une erreur 500 ---
@app.get("/crash")
def crash():
    1 / 0  # Provoque une ZeroDivisionError (erreur 500)

FILE_DB = "recipes.json"

# Modèle de données
class Recipe(BaseModel):
    id: int
    title: str
    ingredients: List[str]
    steps: List[str]
    servings: int
    prep_time_minutes: int

# --- Middleware for logging and metrics ---
@app.middleware("http")
async def log_and_metrics_middleware(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    start_time = time.time()
    endpoint = request.url.path
    logger.info(f"[TRACE_ID={trace_id}] Incoming request: {request.method} {request.url}")
    try:
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
        REQUEST_LATENCY.labels(endpoint).observe(process_time)
        logger.info(f"[TRACE_ID={trace_id}] Response status: {response.status_code} in {process_time:.4f}s")
        response.headers["X-Trace-Id"] = trace_id
        return response
    except Exception as e:
        ERROR_COUNT.labels(endpoint).inc()
        logger.error(f"[TRACE_ID={trace_id}] Error: {e}")
        REQUEST_COUNT.labels(request.method, endpoint, 500).inc()
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error", "trace_id": trace_id})

@app.get("/")
def root():
    trace_id = str(uuid.uuid4())
    return {"message": "Bienvenue sur l'API Recettes Cuisine!", "trace_id": trace_id}


# --- Health check endpoint ---
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

def load_recipes() -> List[Recipe]:
    try:
        with open(FILE_DB, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Recipe(**r) for r in data]
    except FileNotFoundError:
        return []

def save_recipes(recipes: List[Recipe]):
    with open(FILE_DB, "w", encoding="utf-8") as f:
        # FIXED: Use model_dump() instead of dict()
        json.dump([r.model_dump() for r in recipes], f, indent=4, ensure_ascii=False)

# --- Endpoints CRUD ---

@app.get("/recipes", response_model=List[Recipe])
def get_recipes():
    return load_recipes()

@app.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int):
    recipes = load_recipes()
    for r in recipes:
        if r.id == recipe_id:
            return r
    raise HTTPException(status_code=404, detail="Recette non trouvée")

@app.post("/recipes", response_model=Recipe)
def add_recipe(recipe: Recipe):
    recipes = load_recipes()
    if any(r.id == recipe.id for r in recipes):
        raise HTTPException(status_code=400, detail="ID déjà existant")
    recipes.append(recipe)
    save_recipes(recipes)
    return recipe

@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, updated: Recipe):
    recipes = load_recipes()
    for i, r in enumerate(recipes):
        if r.id == recipe_id:
            recipes[i] = updated
            save_recipes(recipes)
            return updated
    raise HTTPException(status_code=404, detail="Recette non trouvée")

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    recipes = load_recipes()
    for r in recipes:
        if r.id == recipe_id:
            recipes.remove(r)
            save_recipes(recipes)
            return {"message": f"Recette {recipe_id} supprimée"}
    raise HTTPException(status_code=404, detail="Recette non trouvée")