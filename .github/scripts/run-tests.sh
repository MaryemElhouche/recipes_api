#!/bin/bash

echo "🧪 Running API tests..."
pytest tests/test_api.py -v --tb=short > pytest-results.txt 2>&1 || true
cat pytest-results.txt