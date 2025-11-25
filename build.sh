#!/bin/bash
# Build script for Render deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Testing imports..."
python test_imports.py || exit 1

echo "Running system setup (scraping + vector store)..."
python scraper.py && python vector_store.py

echo "Build complete! Vector store is ready."
