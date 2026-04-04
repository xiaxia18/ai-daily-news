#!/usr/bin/env python3
"""Debug Alibaba Group careers site."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

url = "https://www.alibabagroup.com/cn/zh/careers/position-search?search=AI"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

print(f"Page loaded, waiting for content...")
time.sleep(20)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

html = driver.page_source
print(f"HTML length: {len(html)}")

soup = BeautifulSoup(html, "lxml")

# Search
all_a = soup.find_all('a', href=True)
job_count = 0
for a in all_a:
    text = a.get_text(strip=True)
    if 'AI' in text or '人工智能' in text:
        job_count += 1
        print(f"Found: {text[:60]}")

print(f"\nFound {job_count} AI links")

# Count classes
from collections import Counter
counter = Counter()
for div in soup.find_all('div'):
    if 'class' in div.attrs:
        for cls in div.attrs['class']:
            counter[cls] += 1

print("\nTop classes with job/item:")
for cls, cnt in counter.most_common(50):
    if any(k in cls.lower() for k in ['job', 'item', 'position', 'card']):
        print(f"  {cls}: {cnt}")

driver.quit()
