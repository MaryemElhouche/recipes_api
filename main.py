import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from loguru import logger
from time import time

app = FastAPI(title="API Recettes Cuisine")

FILE_DB = "recipes.json"

# Modèle de données
class Recipe(BaseModel):
    id: int
    title: str
    ingredients: List[str]
    steps: List[str]
    servings: int
    prep_time_minutes: int

# --- Fonctions utilitaires pour gérer le fichier ---
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Recettes Cuisine!"}

def load_recipes() -> List[Recipe]:
    try:
        with open(FILE_DB, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Recipe(**r) for r in data]
    except FileNotFoundError:
        return []

def save_recipes(recipes: List[Recipe]):
    with open(FILE_DB, "w", encoding="utf-8") as f:
        json.dump([r.dict() for r in recipes], f, indent=4, ensure_ascii=False)

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






