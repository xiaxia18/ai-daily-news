#!/usr/bin/env python3
"""Find correct selector for Tencent jobs."""

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
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

# Get the main content after the search count
found_jobs = []
for a_tag in soup.find_all('a', href=True):
    text = a_tag.get_text(strip=True)
    if 'AI' in text and len(text) > 5:
        parent = a_tag.parent
        if parent.name == 'div':
            grandparent = parent.parent
            if grandparent.name == 'div':
                if 'class' in grandparent.attrs:
                    print(f"Found job: {text[:50]}")
                    print(f"  a tag in div: {'class' in parent.attrs and ' '.join(parent.attrs['class']) or 'no classes'}")
                    print(f"  grandparent div: {'class' in grandparent.attrs and ' '.join(grandparent.attrs['class']) or 'no classes'}")
                    found_jobs.append((text, parent, grandparent))
                    print('-' * 60)

print(f"\nTotal jobs found: {len(found_jobs)}")

# Show full HTML structure of first job
if found_jobs:
    print("\nFull HTML for first job:\n")
    print(found_jobs[0][2].prettify()[:1200])

driver.quit()
