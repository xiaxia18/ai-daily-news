#!/usr/bin/env python3
"""Diagnose Selenium Chrome setup."""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    print("✓ selenium imported successfully")
except ImportError as e:
    print(f"✗ selenium import failed: {e}")
    sys.exit(1)

try:
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    print("✓ Chrome driver started successfully")

    driver.get("https://www.baidu.com")
    print(f"✓ Page loaded, title: {driver.title}")

    driver.quit()
    print("\n✅ Selenium Chrome diagnosis PASSED")
    print("Chrome is working correctly. You can run python main.py now.")

except Exception as e:
    print(f"\n✗ Chrome driver failed: {e}")
    print("\nThis means Chrome is not installed in this environment.")
    print("You need to run this script on your local machine with Chrome installed.")
    sys.exit(1)
