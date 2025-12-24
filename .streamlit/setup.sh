#!/bin/bash
# Setup script for Streamlit Cloud deployment
# This script installs Playwright browsers

echo "Installing Playwright browsers..."
playwright install chromium
echo "Playwright installation complete!"
