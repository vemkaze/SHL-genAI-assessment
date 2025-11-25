#!/bin/bash
# Startup wrapper with error capture

echo "========================================="
echo "Starting SHL Assessment API"
echo "========================================="
echo "Python version:"
python --version
echo ""
echo "Current directory:"
pwd
echo ""
echo "Files present:"
ls -la
echo ""
echo "Environment:"
echo "PORT=$PORT"
echo ""
echo "========================================="

# Try to start uvicorn with error capture
echo "Starting uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port $PORT 2>&1
