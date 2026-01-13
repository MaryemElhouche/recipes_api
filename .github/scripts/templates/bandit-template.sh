#!/bin/bash

cat << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Bandit Security Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #d9534f; border-bottom: 3px solid #d9534f; padding-bottom: 10px; }
        h2 { color: #333; margin-top: 30px; }
        pre { background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 4px; overflow-x: auto; }
        .summary-box { background: #e7f3ff; padding: 15px; border-radius: 4px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Bandit Security Scan Report</h1>
        
        <div class="summary-box">
            <h3>Scan Information</h3>
            <p><strong>Tool:</strong> Bandit</p>
            <p><strong>Scope:</strong> All Python files (excluding tests, venv)</p>
            <p><strong>Generated:</strong> $(date)</p>
        </div>
        
        <h2>📊 Scan Results</h2>
        <pre>$(cat bandit_raw.txt)</pre>
        
        <h2>📄 JSON Output</h2>
        <pre>$(cat bandit_raw.json | python3 -m json.tool 2>/dev/null || cat bandit_raw.json)</pre>
    </div>
</body>
</html>
EOF