#!/usr/bin/env python3
"""Debug new Alibaba talent site."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

url = "https://talent.alibaba.com/?lang=zh#/position/list?keyword=AI"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

print(f"Page loaded, waiting for content...")
time.sleep(20)  # Wait longer for React to load
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

html = driver.page_source
print(f"HTML length: {len(html)}")

soup = BeautifulSoup(html, "lxml")

# Find all divs with job-related classes
print("\n=== Looking for job items ===\n")
from collections import Counter
counter = Counter()
for div in soup.find_all('div'):
    if 'class' in div.attrs:
        for cls in div.attrs['class']:
            counter[cls] += 1

print("Top classes:")
for cls, cnt in counter.most_common(20):
    if any(k in cls.lower() for k in ['job', 'item', 'position', 'list']):
        print(f"  {cls}: {cnt}")

# Find items
all_items = []
for tag in soup.find_all(['div', 'li']):
    if 'class' in tag.attrs:
        classes = ' '.join(tag.attrs['class']).lower()
        if any(k in classes for k in ['job', 'item', 'position']):
            if tag.find(['h1', 'h2', 'h3', 'h4', 'div']):
                all_items.append(tag)

print(f"\nFound {len(all_items)} candidate job items")

# Show first 2
for i, item in enumerate(all_items[:2]):
    if len(all_items) > 0:
        print(f"\n--- Item {i+1} ---\n")
        text = item.get_text(strip=True)
        print(text[:300])

driver.quit()
