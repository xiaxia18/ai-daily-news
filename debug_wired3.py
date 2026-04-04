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
found = first.select("h3[class*='summary-item__hed'] a")
print(f"Found {len(found)} titles with selector h3[class*='summary-item__hed'] a")

if found:
    print(f"Title text: {found[0].get_text(strip=True)}")
    print(f"Href: {found[0].get('href')}")
