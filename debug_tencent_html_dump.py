#!/usr/bin/env python3
"""Dump page HTML to analyze."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = "https://careers.tencent.com/search.html?keyword=AI"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

time.sleep(10)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

html = driver.page_source

with open('/tmp/tencent.html', 'w') as f:
    f.write(html)

print(f"Saved HTML to /tmp/tencent.html ({len(html)} bytes)")

# Find job items by searching for the main list
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')

# Count by class
from collections import Counter
class_counter = Counter()
for div in soup.find_all('div'):
    if 'class' in div.attrs:
        for cls in div.attrs['class']:
            class_counter[cls] += 1

print("\n=== Top 30 most common div classes ===\n")
for cls, count in class_counter.most_common(30):
    print(f"  {cls}: {count}")

driver.quit()
