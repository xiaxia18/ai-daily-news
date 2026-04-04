#!/usr/bin/env python3
"""Debug selenium crawling for Alibaba careers."""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = "https://job.alibaba.com/zhaopin/positionList.htm?keyWord=AI"

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

# Find all divs with class containing 'item' or 'position'
print("\n=== All divs with item/position in class ===\n")
count = 0
for div in soup.find_all('div'):
    if 'class' in div.attrs:
        classes = ' '.join(div.attrs['class']).lower()
        if 'item' in classes or 'position' in classes:
            print(f"  div: {classes}")
            count += 1

print(f"\nFound {count} matching divs")

# Print the job list area
print("\n=== Looking for job list container ===\n")
if soup.body:
    print("Body content length:", len(str(soup.body)))
    # Find any child divs of body that look like a list
    for child in soup.body.children:
        if hasattr(child, 'find_all'):
            job_candidates = child.find_all(['div', 'li'])
            if len(job_candidates) > 10:
                print(f"Found container with {len(job_candidates)} elements")

driver.quit()
