#!/bin/bash
set -e

echo "🛡️ Running OWASP ZAP security scan..."
mkdir -p reports

# Pull ZAP Docker image
docker pull zaproxy/zap-stable

# Run ZAP baseline scan
docker run --network="host" -v $(pwd)/reports:/zap/wrk/:rw \
  zaproxy/zap-stable zap-baseline.py \
  -t http://localhost:8000 \
  -r zap-report.html \
  -J zap-raw.json \
  -w zap-raw.md \
  -d || true

echo "✅ ZAP scan completed: reports/zap-report.html"

# Display summary if available
if [ -f "reports/zap-raw.md" ]; then
  echo "=== ZAP Scan Summary ==="
  cat reports/zap-raw.md
fi