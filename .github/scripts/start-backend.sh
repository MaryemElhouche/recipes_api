#!/bin/bash
set -e

echo "🚀 Starting FastAPI backend..."

# Create empty recipes file
echo "[]" > recipes.json

# Start backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > backend.pid
echo "Backend started with PID: $BACKEND_PID"

# Wait for startup
sleep 10

# Check if process is running
if ps -p $BACKEND_PID > /dev/null 2>&1; then
  echo "✅ Backend process is running"
else
  echo "❌ Backend process died"
  cat backend.log
  exit 1
fi

# Verify backend is responding
echo "🔍 Waiting for backend to be ready..."
SUCCESS=false
for i in {1..30}; do
  echo "Attempt $i/30..."
  if curl -f -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Backend is responding!"
    SUCCESS=true
    break
  fi
  if ! ps -p $(cat backend.pid) > /dev/null 2>&1; then
    echo "❌ Backend died!"
    cat backend.log
    exit 1
  fi
  sleep 2
done

if [ "$SUCCESS" = false ]; then
  echo "❌ Backend not responding"
  cat backend.log
  exit 1
fi