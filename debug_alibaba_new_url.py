#!/usr/bin/env python3
"""Debug Alibaba new website."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Search on Alibaba's new talent site
url = "https://talent.alibaba.com/?lang=zh#/position/list?keyword=AI"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

print(f"Page loaded, waiting...")
time.sleep(25)

for i in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

html = driver.page_source
print(f"HTML length: {len(html)}")

if len(html) > 500:
    soup = BeautifulSoup(html, "lxml")
    print(f"\n=== Looking for job items ===\n")
    count = 0
    for tag in soup.find_all(['div', 'li']):
        if 'class' in tag.attrs:
            classes = ' '.join(tag.attrs['class']).lower()
            if any(k in classes for k in ['job', 'item', 'position', 'card']):
                print(f"  {tag.name}: {classes}")
                count += 1
    print(f"\nFound {count} candidate items")

driver.quit()
