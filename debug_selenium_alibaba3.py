#!/usr/bin/env python3
"""Debug selenium crawling for Alibaba careers on new domain."""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = "https://talent.alibaba.com/off-campus/position-list?lang=zh&keyword=AI"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

print(f"Page loaded, waiting for content...")
time.sleep(15)

# Scroll
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

html = driver.page_source
print(f"HTML length: {len(html)}")

soup = BeautifulSoup(html, "lxml")

# Find all divs with class containing 'item' or 'position' or 'job'
print("\n=== All elements with item/position/job in class ===\n")
count = 0
for tag in soup.find_all(["div", "li"]):
    if 'class' in tag.attrs:
        classes = ' '.join(tag.attrs['class']).lower()
        if 'item' in classes or 'position' in classes or 'job' in classes:
            print(f"  {tag.name}: {classes}")
            count += 1

print(f"\nFound {count} matching elements")

driver.quit()
