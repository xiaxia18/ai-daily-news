#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://www.wired.com/tag/artificial-intelligence/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, verify=False, timeout=30)
soup = BeautifulSoup(response.text, "lxml")

articles = soup.select("div.summary-item")
print(f"Found {len(articles)} articles")

first = articles[0]
print("\nFirst article HTML structure:")
print(first.prettify()[:800])

print("\n--- Testing different selectors ---")
selectors = [
    "a",
    "h3 a",
    "h3[class*='summary-item__hed'] a",
    "div.summary-content a",
]
for selector in selectors:
    found = first.select(selector)
    print(f"  {selector}: {len(found)} found")
    if found:
        print(f"    Text: '{found[0].get_text(strip=True)}'")
