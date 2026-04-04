#!/usr/bin/env python3
"""Debug ByteDance positionItem structure."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

url = "https://jobs.bytedance.com/experienced/position?keywords=AI&city=杭州,上海,广州,北京"

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
soup = BeautifulSoup(html, "lxml")

items = soup.select("div[class*='positionItem']")
print(f"Found {len(items)} positionItem items")

for i, item in enumerate(items[:3]):
    print(f"\n--- Item {i+1} ---\n")
    print(item.prettify()[:1000])

# Check what selectors work for title/desc/link
print("\n--- Checking selectors for first item ---\n")
if items:
    first = items[0]
    title = first.select_one("[class*='title']")
    desc = first.select_one("[class*='jobDesc']")
    a_tag = first.find('a')
    print(f"Title found: {title is not None}")
    if title:
        print(f"Title text: {title.get_text(strip=True)[:80]}")
    print(f"Description found: {desc is not None}")
    if desc:
        print(f"Description: {desc.get_text(strip=True)[:100]}...")
    print(f"a tags: {len(first.find_all('a'))}")
    for a in first.find_all('a'):
        if a.has_attr('href'):
            print(f"  href: {a.get('href')[:80]}")

driver.quit()
