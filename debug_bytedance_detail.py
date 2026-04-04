#!/usr/bin/env python3
"""Debug ByteDance job item structure."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

url = "https://jobs.bytedance.com/experienced/position?keywords=AI"

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
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

items = soup.select("div.positionitem")
print(f"Found {len(items)} div.positionitem items")

for i, item in enumerate(items[:3]):
    print(f"\n--- Item {i+1} ---")
    title_elem = item.select_one("div.title")
    jobdesc_elem = item.select_one("div.jobdesc")
    a_tags = item.find_all('a')
    print(f"  Title found: {title_elem is not None}")
    if title_elem:
        print(f"  Title text: {title_elem.get_text(strip=True)}")
    print(f"  Description found: {jobdesc_elem is not None}")
    if jobdesc_elem:
        print(f"  Description: {jobdesc_elem.get_text(strip=True)[:100]}")
    print(f"  Number of a tags: {len(a_tags)}")
    for a in a_tags:
        if a.has_attr('href'):
            print(f"    href: {a.get('href')[:100]}")

driver.quit()
