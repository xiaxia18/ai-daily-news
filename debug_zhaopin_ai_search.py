#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://sou.zhaopin.com/?jl=650%2C680%2C630%2C70%2C7630&kw=AI&kt=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

response = requests.get(url, verify=False, timeout=30, headers=headers)
print(f"Status: {response.status_code}")
print(f"Length: {len(response.text)}")

if len(response.text) > 5000:
    soup = BeautifulSoup(response.text, "lxml")
    items = soup.select(".position-list-item")
    print(f"Found {len(items)} .position-list-item")

    if items:
        print(f"\nFirst item:\n{items[0].prettify()[:800]}")
