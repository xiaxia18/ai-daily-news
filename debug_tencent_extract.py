#!/usr/bin/env python3
"""Debug Tencent extraction."""

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

time.sleep(10)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

items = soup.select("div.recruit-list")
print(f"Found {len(items)} recruit-list items")

for i, item in enumerate(items):
    print(f"\n=== Item {i+1} ===")
    a_tags = item.find_all('a')
    print(f"Number of a tags: {len(a_tags)}")
    for a in a_tags:
        href = a.get('href')
        title = a.get_text(strip=True)
        print(f"  a tag: href='{href[:80] if href else 'NO HREF'}...', title='{title[:60] if title else 'NO TITLE'}...'")

driver.quit()
