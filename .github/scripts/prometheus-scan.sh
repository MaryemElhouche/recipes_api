#!/bin/bash
set -e

echo "📊 Collecting Prometheus metrics..."
mkdir -p reports

# Test metrics endpoint
if ! curl -f http://localhost:8000/metrics > /dev/null 2>&1; then
  echo "❌ Metrics endpoint failed"
  exit 1
fi

echo "✅ Metrics endpoint is working"

# Generate test traffic
echo "Generating test traffic..."
curl -s http://localhost:8000/ > /dev/null
curl -s http://localhost:8000/recipes > /dev/null
curl -s http://localhost:8000/recipes/1 > /dev/null || true
curl -s http://localhost:8000/metrics > /dev/null

sleep 2

# Collect final metrics
curl -f http://localhost:8000/metrics > metrics_raw.txt

# Generate HTML report using template
bash .github/scripts/templates/prometheus-template.sh > reports/prometheus-report.html

echo "✅ Prometheus report generated: reports/prometheus-report.html"