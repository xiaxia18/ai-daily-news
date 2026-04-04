#!/usr/bin/env python3
"""Debug Tencent find where URL is stored."""

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
item = items[0]

print("Full outer HTML of first job:")
print(item.prettify()[:800])

# Check all elements for URL-like attributes
print("\n\nChecking all elements for data-* attributes:")
for elem in item.find_all(True):
    for attr_name, attr_value in elem.attrs.items():
        if attr_name.startswith('data-') or 'url' in attr_name.lower() or 'link' in attr_name.lower():
            print(f"  {elem.name}[{attr_name}] = {attr_value}")
    if elem.name == 'a' and elem.attrs:
        print(f"  a attrs: {list(elem.attrs.keys())}")

driver.quit()
