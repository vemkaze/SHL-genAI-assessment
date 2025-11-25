#!/bin/bash
# Unix/Linux/Mac setup script

set -e

echo "============================================================"
echo "SHL Assessment Recommendation System - Quick Setup"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt

echo "[4/5] Setting up environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Please edit .env and add your GEMINI_API_KEY"
    read -p "Press Enter after editing .env..."
fi

echo "[5/5] Running setup script..."
python setup.py

echo ""
echo "============================================================"
echo "Setup complete!"
echo ""
echo "To start the server:"
echo "  python main.py"
echo ""
echo "Then open: http://localhost:8000"
echo "============================================================"
