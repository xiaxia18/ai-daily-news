#!/usr/bin/env python3
"""Find URL in Tencent share button."""

import time
import re
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
for i, item in enumerate(items[:3]):
    print(f"\n--- Item {i+1} ---")
    # Look at the title
    title_span = item.select_one("span.job-recruit-title")
    if title_span:
        title_text = title_span.get_text(strip=True)
        print(f"Title: {title_text}")
        # Try to find postId
        match = re.search(r' (\d+)$', title_text)
        if match:
            post_id = match.group(1)
            constructed_url = f"https://careers.tencent.com/jobdesc.html?postId={post_id}"
            print(f"Constructed URL: {constructed_url}")

driver.quit()
