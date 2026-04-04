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
title_selector = "h3.summary-item__hed a"
title_elem = first.select_one(title_selector)
print(f"\nLooking for {title_selector} in first article: found={title_elem}")

if title_elem:
    print(f"Title text: {title_elem.get_text(strip=True)}")

# Print the classes found in first article
print("\nClasses in first article:")
for tag in first.find_all(True):
    if 'class' in tag.attrs:
        print(f"  {tag.name}: {tag.attrs['class']}")
