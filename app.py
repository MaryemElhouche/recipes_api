import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recipes"  # URL de ton API FastAPI

st.set_page_config(page_title="Recettes de Cuisine", layout="wide")

st.title("🍳 Recettes de Cuisine")

# --- Fonctions CRUD via API ---
def get_recipes():
    resp = requests.get(API_URL, timeout=5)
    if resp.status_code == 200:
        return resp.json()
    return []

def get_recipe(recipe_id):
    resp = requests.get(f"{API_URL}/{recipe_id}", timeout=5)
    if resp.status_code == 200:
        return resp.json()
    return None

def add_recipe(data):
    resp = requests.post(API_URL, json=data, timeout=5)
    return resp

def update_recipe(recipe_id, data):
    resp = requests.put(f"{API_URL}/{recipe_id}", json=data, timeout=5)
    return resp

def delete_recipe(recipe_id):
    resp = requests.delete(f"{API_URL}/{recipe_id}", timeout=5)
    return resp

# --- Interface Streamlit ---

menu = ["Voir Recettes", "Ajouter Recette", "Modifier Recette", "Supprimer Recette"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Voir Recettes":
    st.subheader("📋 Liste des recettes")
    recipes = get_recipes()
    for r in recipes:
        with st.expander(f"{r['title']} (Pour {r['servings']} personnes)"):
            st.markdown(f"**ID:** {r['id']}")
            st.markdown(f"**Temps de préparation:** {r['prep_time_minutes']} minutes")
            st.markdown("**Ingrédients:**")
            st.write(r['ingredients'])
            st.markdown("**Étapes:**")
            for i, step in enumerate(r['steps'], 1):
                st.write(f"{i}. {step}")

elif choice == "Ajouter Recette":
    st.subheader("➕ Ajouter une nouvelle recette")
    with st.form("add_form"):
        title = st.text_input("Titre")
        ingredients = st.text_area("Ingrédients (séparés par des virgules)")
        steps = st.text_area("Étapes (séparées par des virgules)")
        servings = st.number_input("Nombre de personnes", min_value=1, value=2)
        prep_time = st.number_input("Temps de préparation (minutes)", min_value=1, value=15)
        recipe_id = st.number_input("ID de la recette", min_value=1, value=100)
        submitted = st.form_submit_button("Ajouter")
        if submitted:
            data = {
                "id": recipe_id,
                "title": title,
                "ingredients": [i.strip() for i in ingredients.split(",")],
                "steps": [s.strip() for s in steps.split(",")],
                "servings": servings,
                "prep_time_minutes": prep_time
            }
            resp = add_recipe(data)
            if resp.status_code == 200:
                st.success("Recette ajoutée avec succès !")
            else:
                st.error(f"Erreur : {resp.json()['detail']}")

elif choice == "Modifier Recette":
    st.subheader("✏️ Modifier une recette existante")
    recipes = get_recipes()
    recipe_ids = [r['id'] for r in recipes]
    selected_id = st.selectbox("Sélectionner la recette à modifier (ID)", recipe_ids)
    recipe = get_recipe(selected_id)
    if recipe:
        with st.form("update_form"):
            title = st.text_input("Titre", recipe['title'])
            ingredients = st.text_area("Ingrédients (séparés par des virgules)", ",".join(recipe['ingredients']))
            steps = st.text_area("Étapes (séparées par des virgules)", ",".join(recipe['steps']))
            servings = st.number_input("Nombre de personnes", min_value=1, value=recipe['servings'])
            prep_time = st.number_input("Temps de préparation (minutes)", min_value=1, value=recipe['prep_time_minutes'])
            submitted = st.form_submit_button("Mettre à jour")
            if submitted:
                data = {
                    "id": recipe['id'],
                    "title": title,
                    "ingredients": [i.strip() for i in ingredients.split(",")],
                    "steps": [s.strip() for s in steps.split(",")],
                    "servings": servings,
                    "prep_time_minutes": prep_time
                }
                resp = update_recipe(selected_id, data)
                if resp.status_code == 200:
                    st.success("Recette mise à jour avec succès !")
                else:
                    st.error(f"Erreur : {resp.json()['detail']}")

elif choice == "Supprimer Recette":
    st.subheader("🗑️ Supprimer une recette")
    recipes = get_recipes()
    recipe_ids = [r['id'] for r in recipes]
    selected_id = st.selectbox("Sélectionner la recette à supprimer (ID)", recipe_ids)
    if st.button("Supprimer"):
        resp = delete_recipe(selected_id)
        if resp.status_code == 200:
            st.success(resp.json()["message"])
        else:
            st.error(f"Erreur : {resp.json()['detail']}")


