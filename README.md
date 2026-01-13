# DevOps Project: Recipe API & Frontend

## Overview
This project demonstrates end-to-end DevOps practices by designing, building, and deploying a small backend REST API and a Streamlit frontend. The project covers coding, containerization, automation, deployment, observability, and security.

## Features
- **Backend:** FastAPI REST API for recipe CRUD operations
- **Frontend:** Streamlit web app for interacting with the API
- **Observability:** Prometheus metrics, structured logs, basic tracing
- **Security:** SAST (Bandit) and DAST (OWASP ZAP) integrated in CI
- **Testing:** Pytest for backend, Selenium for frontend
- **Containerization:** Dockerfile and docker-compose for local orchestration
- **CI/CD:** GitHub Actions for build, test, security scan, and deployment

## Project Structure
```
app.py                  # Streamlit frontend
main.py                 # FastAPI backend
metrics_initializer.py  # Prometheus metrics setup
recipes.json            # Sample recipe data
requirements.txt        # Python dependencies
Dockerfile              # API Docker build
prometheus.yml          # Prometheus config
.github/workflows/      # CI/CD workflows
```

## Setup Instructions
### 1. Clone the Repository
```
git clone https://github.com/MaryemElhouche/recipes_api
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Run Locally
- **Start API:**
  ```
  uvicorn main:app --reload
  ```
- **Start Frontend:**
  ```
  streamlit run app.py
  ```
- **Access:**
  - API: http://localhost:8000
  - Frontend: http://localhost:8501

### 4. Run with Docker Compose
```
docker-compose up --build
```
- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## API Examples
- **List Recipes:** `GET /recipes`
- **Get Recipe:** `GET /recipes/{id}`
- **Add Recipe:** `POST /recipes`
- **Update Recipe:** `PUT /recipes/{id}`
- **Delete Recipe:** `DELETE /recipes/{id}`
- **Metrics:** `GET /metrics`

## Observability
- **Metrics:** Prometheus endpoint at `/metrics`
- **Logs:** Structured logs with trace IDs
- **Tracing:** Trace IDs in logs and responses

## Security
- **SAST:** Bandit runs in CI
- **DAST:** OWASP ZAP scans both backend and frontend in CI, reports uploaded as artifacts

## CI/CD Pipeline
- **CI:**
  - Lint, test, SAST, DAST, and artifact upload
- **CD:**
  - Docker build and push to Docker Hub

## Kubernetes 


## Documentation & Reporting
- All setup, usage, and security scan results are documented here.
- For more details, see the final report in the repo.

## Author
- Maryem Elhouche

