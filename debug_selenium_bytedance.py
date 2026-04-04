#!/usr/bin/env python3
"""Debug selenium crawling for Bytedance careers."""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = "https://jobs.bytedance.com/experienced/position?keywords=AI"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

print(f"Page loaded, waiting for content...")
time.sleep(10)

# Scroll
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

html = driver.page_source
print(f"HTML length: {len(html)}")

soup = BeautifulSoup(html, "lxml")

# Search for any job-like items
print("\n=== Looking for job containers ===\n")
job_count = 0
for tag in soup.find_all(["div", "li"]):
    if 'class' in tag.attrs:
        classes = ' '.join(tag.attrs['class']).lower()
        if 'job' in classes or 'post' in classes or 'position' in classes or 'item' in classes:
            print(f"  {tag.name}: {classes}")
            job_count += 1

print(f"\nFound {job_count} candidate elements")

# Print first 5000 chars to see structure
print("\n=== HTML Preview (first 5000 chars) ===\n")
print(html[:5000])

driver.quit()
