#!/usr/bin/env python3
"""Try to extract all jobs for ByteDance."""

import time
import re
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

time.sleep(20)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

# Find top level positionItem that contains everything
items = soup.find_all('div', class_='positionItem')
print(f"Found {len(items)} top-level positionItem")

success_count = 0
for i, item in enumerate(items):
    title_elem = item.select_one("span.positionItem-title-text")
    desc_elem = item.select_one("div[class*='jobDesc']")

    title = title_elem.get_text(strip=True) if title_elem else None
    desc = desc_elem.get_text(strip=False) if desc_elem else None

    all_text = item.get_text(strip=False)
    match = re.search(r'职位\s*ID[：:]\s*([A-Za-z0-9]+)', all_text)
    if match:
        job_id = match.group(1)
        url = f"https://jobs.bytedance.com/experienced/position/{job_id}"
        print(f"\n✅ Job {i+1}:")
        print(f"  Title: {title}")
        print(f"  JobId: {job_id}")
        print(f"  URL: {url}")
        if desc:
            print(f"  Desc: {desc[:150]}...")
        success_count += 1
    else:
        print(f"\n❌ Job {i+1}: no ID match")
        print(f"  Title: {title}")
        print(f"  All text length: {len(all_text)}")
        if len(all_text) < 200:
            print(f"  Text: {repr(all_text)}")

print(f"\nTotal: {success_count}/{len(items)} jobs successfully extracted")

driver.quit()
