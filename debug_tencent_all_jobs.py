#!/usr/bin/env python3
"""Debug Tencent show full job list HTML."""

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

print(f"Page loaded, waiting for content...")
time.sleep(10)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

# Find the main content area
print("\n=== Scanning for job list ===\n")
all_divs = soup.find_all('div')
job_list_found = None
for div in all_divs:
    if 'class' in div.attrs:
        classes = ' '.join(div.attrs['class']).lower()
        if 'list' in classes and 'job' in classes:
            print(f"Found job list container: {classes}")
            job_list_found = div
            break

if job_list_found:
    print("\n=== Job list content, first 2000 chars ===\n")
    print(str(job_list_found)[:3000])
else:
    # Just search for anything with "AI" in text
    print("\n=== Looking for any AI text in page ===\n")
    text = soup.get_text()
    lines = text.split('\n')
    ai_lines = [line.strip() for line in lines if 'AI' in line or '人工智能' in line][:20]
    for line in ai_lines:
        print(line)

driver.quit()
