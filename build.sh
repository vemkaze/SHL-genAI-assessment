#!/bin/bash
# Build script for Render deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running system setup (scraping + vector store)..."
python scraper.py && python vector_store.py

echo "Build complete! Vector store is ready."
