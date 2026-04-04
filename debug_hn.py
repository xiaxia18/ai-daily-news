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

# Find all links that contain "hiring" or "ai" in title
for thing in things[:5]:
    title_link = thing.select_one("a.storylink")
    if title_link:
        print(f"  Title: {title_link.get_text(strip=True)}")
        print(f"  URL: {title_link.get('href')}")
