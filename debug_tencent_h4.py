#!/usr/bin/env python3
"""Debug Tencent find h4 tags."""

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

time.sleep(8)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

all_h4 = soup.find_all('h4')
print(f"Found {len(all_h4)} h4 tags")

for i, h4 in enumerate(all_h4):
    print(f"\n--- h4 {i+1} ---")
    print(f"Text: {h4.get_text(strip=True)}")

    # Walk up to find the outer container
    node = h4
    while node.parent:
        if node.name == 'div' and 'class' in node.attrs:
            classes = ' '.join(node.attrs['class'])
            print(f"Parent div classes: {classes}")
        node = node.parent
        if node.name == 'body':
            break

driver.quit()
