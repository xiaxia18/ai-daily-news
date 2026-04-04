#!/usr/bin/env python3
"""Debug Baidu careers page with longer wait."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

url = "https://talent.baidu.com/jobs/list?keyword=AI"

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)

print("Getting page...")
driver.get(url)

print(f"Current URL after load: {driver.current_url}")
print(f"Page title: {driver.title}")

# Wait and scroll
print("Waiting 30 seconds for JS to load...")
time.sleep(30)

for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

html = driver.page_source
print(f"HTML length after wait: {len(html)}")

if len(html) > 100:
    soup = BeautifulSoup(html, "lxml")
    items = soup.select('li')
    print(f"Found {len(items)} li elements")
    with open('/tmp/baidu.html', 'w') as f:
        f.write(html)
    print(f"Saved full HTML to /tmp/baidu.html")

driver.quit()
