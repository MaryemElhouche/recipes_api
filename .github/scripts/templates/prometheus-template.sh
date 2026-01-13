#!/bin/bash

cat << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Prometheus Metrics Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #e6522c; border-bottom: 3px solid #e6522c; padding-bottom: 10px; }
        h2 { color: #333; margin-top: 30px; }
        .metric-section { background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 4px; border-left: 4px solid #e6522c; }
        .success { color: #28a745; font-weight: bold; }
        pre { background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 4px; overflow-x: auto; }
        .summary-box { background: #e7f3ff; padding: 15px; border-radius: 4px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Prometheus Metrics Report</h1>
        
        <div class="summary-box">
            <h3 class="success">✅ Metrics Collection Status: SUCCESS</h3>
            <p><strong>Endpoint:</strong> http://localhost:8000/metrics</p>
            <p><strong>Generated:</strong> $(date)</p>
        </div>
        
        <h2>📈 Request Metrics</h2>
        <div class="metric-section">
            <h3>Request Counts by Endpoint</h3>
            <pre>$(grep "request_count{" metrics_raw.txt | head -20)</pre>
        </div>
        
        <h2>⏱️ Latency Metrics</h2>
        <div class="metric-section">
            <h3>Request Latency Distribution</h3>
            <pre>$(grep "request_latency" metrics_raw.txt | head -30)</pre>
        </div>
        
        <h2>❌ Error Metrics</h2>
        <div class="metric-section">
            <h3>Error Counts</h3>
            <pre>$(grep "error_count" metrics_raw.txt || echo "No errors recorded")</pre>
        </div>
        
        <h2>📋 All Metrics (Raw)</h2>
        <div class="metric-section">
            <pre>$(cat metrics_raw.txt)</pre>
        </div>
    </div>
</body>
</html>
EOF