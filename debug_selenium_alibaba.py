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
time.sleep(10)

# Scroll
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

html = driver.page_source
print(f"HTML length: {len(html)}")

soup = BeautifulSoup(html, "lxml")

# Search for table rows
print("\n=== Looking for table rows ===\n")
table_rows = soup.find_all('tr')
print(f"Total tr elements: {len(table_rows)}")
for i, tr in enumerate(table_rows):
    if 'class' in tr.attrs:
        classes = ' '.join(tr.attrs['class']).lower()
        print(f"  tr[{i}]: {classes}")

# Search for any job-like items
print("\n=== Looking for job containers ===\n")
job_count = 0
for tag in soup.find_all(["div", "li", "tr", "td"]):
    if 'class' in tag.attrs:
        classes = ' '.join(tag.attrs['class']).lower()
        if 'job' in classes or 'post' in classes or 'position' in classes or 'item' in classes or 'even' in classes or 'odd' in classes:
            print(f"  {tag.name}: {classes}")
            job_count += 1

print(f"\nFound {job_count} candidate elements")

driver.quit()
