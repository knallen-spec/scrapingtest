"""
Setup script to install Playwright browsers on first run
"""
import subprocess
import sys
import os

def install_playwright_browsers():
    """Install Playwright browsers if not already installed."""
    try:
        # Check if chromium is already installed
        cache_dir = os.path.expanduser("~/.cache/ms-playwright")

        if not os.path.exists(cache_dir) or not os.listdir(cache_dir):
            print("Installing Playwright browsers...")
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
            subprocess.check_call([sys.executable, "-m", "playwright", "install-deps", "chromium"])
            print("Playwright browsers installed successfully!")
        else:
            print("Playwright browsers already installed.")

    except Exception as e:
        print(f"Warning: Could not install Playwright browsers: {e}")

if __name__ == "__main__":
    install_playwright_browsers()
