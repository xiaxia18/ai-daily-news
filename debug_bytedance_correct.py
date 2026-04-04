#!/usr/bin/env python3
"""Debug ByteDance correct job list structure."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Search AI and filter to 杭州/上海/广州/北京
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
print(f"HTML length: {len(html)}")

soup = BeautifulSoup(html, "lxml")

# Count elements containing positionitem
print("\n=== Searching for positionitem classes ===\n")
all_divs = soup.find_all('div')
count = 0
for div in all_divs:
    if 'class' in div.attrs:
        classes = ' '.join(div.attrs['class'])
        if 'positionitem' in classes:
            count += 1
            if count <= 3:
                print(f"\n--- Item {count} ---\n")
                print(div.prettify()[:800])

print(f"\nFound {count} positionitem elements")

# List all classes that contain 'position'
print("\n=== All div classes containing 'position' ===\n")
position_classes = set()
for div in all_divs:
    if 'class' in div.attrs:
        for cls in div.attrs['class']:
            if 'position' in cls.lower():
                position_classes.add(cls)

for cls in sorted(position_classes):
    print(f"  {cls}")

driver.quit()
