#!/usr/bin/env python3
"""Debug selenium crawling for Tencent careers."""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = "https://careers.tencent.com/search.html?keyword=AI"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shim-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

print(f"Page loaded, waiting for content...")
time.sleep(8)

# Scroll
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

html = driver.page_source
print(f"HTML length: {len(html)}")

soup = BeautifulSoup(html, "lxml")

# Search for any job-like items
print("\n=== Looking for job containers ===")
for tag in soup.find_all(["div", "li"]):
    if 'class' in tag.attrs:
        classes = ' '.join(tag.attrs['class']).lower()
        if 'job' in classes or 'position' in classes or 'item' in classes:
            print(f"  {tag.name}: {classes}")

# Print first 2000 chars to see structure
print("\n=== HTML Preview ===")
print(html[:3000])

driver.quit()
