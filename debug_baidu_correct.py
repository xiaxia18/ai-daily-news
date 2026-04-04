#!/usr/bin/env python3
"""Debug Baidu careers page."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Search AI in Beijing/Shanghai/Guangzhou/Hangzhou
url = "https://talent.baidu.com/jobs/list?keyword=AI"

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

# Scroll down to load content
for i in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

html = driver.page_source
print(f"HTML length: {len(html)}")

if len(html) < 100:
    print(f"Empty HTML: {html}")
else:
    soup = BeautifulSoup(html, "lxml")
    print(f"\nBody length: {len(str(soup.body)) if soup.body else 0}")

    # Find all job items
    print("\n=== Looking for job items ===\n")
    all_items = []
    for tag in soup.find_all(['div', 'li']):
        if 'class' in tag.attrs:
            classes = ' '.join(tag.attrs['class']).lower()
            if any(k in classes for k in ['job', 'item', 'position']):
                print(f"  {tag.name}: {classes}")
                all_items.append(tag)

    print(f"\nFound {len(all_items)} candidate items")

    # Show first item
    if len(all_items) > 0:
        print("\n=== First item HTML ===\n")
        print(all_items[0].prettify()[:1000])

driver.quit()
