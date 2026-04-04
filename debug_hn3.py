#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://news.ycombinator.com/submitted?id=whoishiring"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, verify=False, timeout=30)
soup = BeautifulSoup(response.text, "lxml")

things = soup.select("tr.athing")
print(f"Found {len(things)} tr.athing")

for i, thing in enumerate(things[:3]):
    print(f"\n--- Article {i+1} ---")
    title_selector = "td.title a.storylink"
    title_elem = thing.select_one(title_selector)
    print(f"  Selector '{title_selector}' found: {title_elem}")
    if title_elem:
        print(f"  Title: '{title_elem.get_text(strip=True)}'")
        print(f"  URL: {title_elem.get('href')}")
