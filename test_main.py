import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- Données de test ---
test_recipe = {
    "id": 999,
    "title": "Test Recette",
    "ingredients": ["Ingredient1", "Ingredient2"],
    "steps": ["Step1", "Step2"],
    "servings": 2,
    "prep_time_minutes": 10
}

# --- Tests ---

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Bienvenue" in response.json()["message"]

def test_get_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_recipe():
    response = client.post("/recipes", json=test_recipe)
    assert response.status_code == 200
    assert response.json()["id"] == test_recipe["id"]

def test_post_duplicate_recipe():
    response = client.post("/recipes", json=test_recipe)
    assert response.status_code == 400

def test_get_recipe():
    response = client.get(f"/recipes/{test_recipe['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == test_recipe["title"]

def test_put_recipe():
    updated_recipe = test_recipe.copy()
    updated_recipe["title"] = "Updated Test Recette"
    response = client.put(f"/recipes/{test_recipe['id']}", json=updated_recipe)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Recette"

def test_delete_recipe():
    response = client.delete(f"/recipes/{test_recipe['id']}")
    assert response.status_code == 200
    assert "supprimée" in response.json()["message"]
