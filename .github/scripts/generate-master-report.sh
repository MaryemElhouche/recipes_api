#!/bin/bash
set -e

echo "📋 Generating master security report..."

# Use template to generate master report
bash .github/scripts/templates/master-report-template.sh > reports/MASTER-SECURITY-REPORT.html

echo "✅ Master report generated: reports/MASTER-SECURITY-REPORT.html"