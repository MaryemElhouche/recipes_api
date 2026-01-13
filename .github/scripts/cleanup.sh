#!/bin/bash

echo "🧹 Cleaning up..."
if [ -f backend.pid ]; then
  kill $(cat backend.pid) 2>/dev/null || true
  echo "Backend process stopped"
fi

if [ -f backend.log ]; then
  echo "=== Final Backend Log (last 50 lines) ==="
  tail -50 backend.log
fi