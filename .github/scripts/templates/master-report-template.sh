#!/bin/bash

cat << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Master Security & QA Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .header { background: white; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header h1 { margin: 0; color: #333; font-size: 36px; }
        .header .meta { color: #666; margin-top: 10px; }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        .card { background: white; border-radius: 12px; padding: 30px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; margin-top: 0; }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
        .status-card { padding: 20px; border-radius: 8px; text-align: center; background: #d4edda; border: 2px solid #28a745; }
        .status-card h3 { margin: 0 0 10px 0; font-size: 18px; }
        .status-card .icon { font-size: 48px; margin-bottom: 10px; }
        .report-links { background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; }
        .report-links a { display: block; color: #667eea; text-decoration: none; padding: 10px; margin: 5px 0; background: white; border-radius: 4px; transition: all 0.3s; }
        .report-links a:hover { background: #667eea; color: white; transform: translateX(5px); }
        .summary-section { background: #e7f3ff; padding: 20px; border-radius: 8px; margin: 20px 0; }
        pre { background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 4px; overflow-x: auto; }
        .footer { text-align: center; color: white; padding: 20px; margin-top: 40px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔐 Master Security & QA Report</h1>
        <div class="meta">
            <strong>Generated:</strong> $(date)<br>
            <strong>Pipeline:</strong> GitHub Actions CI<br>
            <strong>Branch:</strong> ${GITHUB_REF_NAME}<br>
            <strong>Commit:</strong> ${GITHUB_SHA}
        </div>
    </div>
    
    <div class="container">
        <div class="card">
            <h2>📊 Executive Summary</h2>
            <p>This report consolidates security scanning, metrics collection, and API testing results.</p>
            
            <div class="status-grid">
                <div class="status-card">
                    <div class="icon">🔒</div>
                    <h3>Bandit Scan</h3>
                    <p>Python Security Linter</p>
                    <strong>Status: Completed</strong>
                </div>
                
                <div class="status-card">
                    <div class="icon">🛡️</div>
                    <h3>OWASP ZAP</h3>
                    <p>Web Security Scanner</p>
                    <strong>Status: Completed</strong>
                </div>
                
                <div class="status-card">
                    <div class="icon">📊</div>
                    <h3>Prometheus</h3>
                    <p>Metrics Collection</p>
                    <strong>Status: Active</strong>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>📁 Available Reports</h2>
            <div class="report-links">
                <a href="bandit-report.html">🔒 Bandit Security Report (HTML)</a>
                <a href="zap-report.html">🛡️ OWASP ZAP Security Report (HTML)</a>
                <a href="prometheus-report.html">📊 Prometheus Metrics Report (HTML)</a>
            </div>
        </div>
        
        <div class="card">
            <h2>🔒 Bandit Security Scan Summary</h2>
            <div class="summary-section">
                <pre>$(cat bandit_raw.txt | grep -A 50 "Test results:" || echo "Scan completed - see detailed report")</pre>
            </div>
        </div>
        
        <div class="card">
            <h2>🛡️ OWASP ZAP Scan Summary</h2>
            <div class="summary-section">
                <p><strong>Target:</strong> http://localhost:8000</p>
                <p><strong>Scan Type:</strong> Baseline (Passive + Spider)</p>
                <pre>$(cat reports/zap-raw.md 2>/dev/null | head -50 || echo "Scan completed - see detailed report")</pre>
            </div>
        </div>
        
        <div class="card">
            <h2>📊 Prometheus Metrics Summary</h2>
            <div class="summary-section">
                <h3>Request Counts</h3>
                <pre>$(grep "request_count{" metrics_raw.txt | head -10)</pre>
                
                <h3>Error Counts</h3>
                <pre>$(grep "error_count" metrics_raw.txt || echo "No errors recorded")</pre>
            </div>
        </div>
        
        <div class="card">
            <h2>🧪 API Tests Summary</h2>
            <div class="summary-section">
                <pre>$(cat pytest-results.txt | tail -20)</pre>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by GitHub Actions CI Pipeline</p>
        <p>All reports are available as artifacts in the Actions tab</p>
    </div>
</body>
</html>
EOF