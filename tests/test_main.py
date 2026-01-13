import pytest
import sys
import os

# Add parent directory to path so we can import main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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


# --- Additional Tests ---
def test_health():
    """Test the /health endpoint returns status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_nonexistent_recipe():
    """Test getting a non-existent recipe returns 404."""
    response = client.get("/recipes/123456789")
    assert response.status_code == 404

def test_update_nonexistent_recipe():
    """Test updating a non-existent recipe returns 404."""
    fake_recipe = test_recipe.copy()
    fake_recipe["id"] = 123456789
    response = client.put(f"/recipes/123456789", json=fake_recipe)
    assert response.status_code == 404

def test_delete_nonexistent_recipe():
    """Test deleting a non-existent recipe returns 404."""
    response = client.delete("/recipes/123456789")
    assert response.status_code == 404

def test_crash_endpoint():
    """Test the /crash endpoint returns 500 error."""
    response = client.get("/crash")
    assert response.status_code == 500