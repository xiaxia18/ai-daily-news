#!/usr/bin/env python3
"""Debug ByteDance URL extraction."""

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

items = soup.select("div[class*='positionItem']")
print(f"Found {len(items)} items")

success = 0
for i, item in enumerate(items[:10]):
    all_text = item.get_text(strip=False)
    match = re.search(r'职位\s*ID[：:]\s*([A-Za-z0-9]+)', all_text)
    if match:
        job_id = match.group(1)
        url = f"https://jobs.bytedance.com/experienced/position/{job_id}"
        title_elem = item.select_one("span.positionItem-title-text")
        title = title_elem.get_text(strip=True) if title_elem else "NO TITLE"
        desc_elem = item.select_one("div[class*='jobDesc']")
        desc = desc_elem.get_text(strip=False)[:100] if desc_elem else "NO DESC"
        print(f"\n✅ Item {i+1}:")
        print(f"  Title: {title}")
        print(f"  JobId: {job_id}")
        print(f"  URL: {url}")
        print(f"  Description: {desc[:100]}...")
        success += 1
    else:
        print(f"\n❌ Item {i+1}: NO job ID found")
        print(f"  Text snippet: {all_text[-100:]}")

print(f"\nTotal success: {success}/{len(items[:10])}")

driver.quit()
