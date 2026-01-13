#!/bin/bash
set -e

echo "🔒 Running Bandit security scan..."
mkdir -p reports

# Run Bandit scans
bandit -r . -f txt --exclude ./tests,./venv,./.git > bandit_raw.txt 2>&1 || true
bandit -r . -f json --exclude ./tests,./venv,./.git > bandit_raw.json 2>&1 || true

# Generate HTML report using template
bash .github/scripts/templates/bandit-template.sh > reports/bandit-report.html

echo "✅ Bandit report generated: reports/bandit-report.html"
echo "=== Bandit Summary ==="
cat bandit_raw.txt