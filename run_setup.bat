@echo off
REM Windows batch script to run the complete setup

echo ============================================================
echo SHL Assessment Recommendation System - Quick Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Setting up environment file...
if not exist ".env" (
    copy .env.example .env
    echo Please edit .env and add your GEMINI_API_KEY
    echo Press any key after editing .env...
    pause >nul
)

echo [5/5] Running setup script...
python setup.py

echo.
echo ============================================================
echo Setup complete!
echo.
echo To start the server:
echo   python main.py
echo.
echo Then open: http://localhost:8000
echo ============================================================
pause
