#!/bin/bash
# Quick start script for the web interface

echo "========================================"
echo "Google Maps Company Scraper - Web UI"
echo "========================================"
echo ""

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    playwright install chromium
fi

echo "Starting web interface..."
echo "Opening browser to http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

streamlit run app.py
