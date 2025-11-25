#!/bin/bash
# Build script for Render deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running system setup..."
python setup.py

echo "Build complete!"
