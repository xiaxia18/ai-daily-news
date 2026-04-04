#!/usr/bin/env python3
"""Debug Tencent real job items."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

url = "https://careers.tencent.com/search.html?keyword=AI"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

print(f"Page loaded, waiting for content...")
time.sleep(8)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

# Search for items
print("\n=== Searching for job containers ===\n")
all_divs = soup.find_all('div')
for div in all_divs:
    if 'class' in div.attrs:
        classes = ' '.join(div.attrs['class'])
        if 'job' in classes.lower() or 'search' in classes.lower():
            print(f"div: {classes}")

# Find the real job list
print("\n=== Finding job items ===\n")
job_items = soup.select('div[class*="item"]')
print(f"Found {len(job_items)} items with 'item' in class")
for i, item in enumerate(job_items):
    if 'class' in item.attrs:
        classes = ' '.join(item.attrs['class'])
        # Check if it contains a h4 (which should be the title)
        if item.find('h4'):
            print(f"Item {i}: classes={classes}, has h4 title")

# Show the first 3 real items
print("\n=== First 3 real job items HTML ===\n")
count = 0
parent_classes = []
for item in job_items:
    if item.find('h4'):
        parent = item.parent
        if parent and 'class' in parent.attrs:
            p_classes = ' '.join(parent.attrs['class'])
            parent_classes.append(p_classes)
            print(f"Parent classes: {p_classes}")
        if count < 3:
            print(item.prettify()[:1000])
            print('\n' + '='*80 + '\n')
            count += 1

print(f"\nAll parent classes with items containing h4: {parent_classes}")

driver.quit()
