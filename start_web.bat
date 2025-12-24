@echo off
REM Quick start script for Windows

echo ========================================
echo Google Maps Company Scraper - Web UI
echo ========================================
echo.

REM Check if dependencies are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    playwright install chromium
)

echo Starting web interface...
echo Opening browser to http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

streamlit run app.py
