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
print(f"Status: {response.status_code}")
soup = BeautifulSoup(response.text, "lxml")

articles = soup.select("div.summary-item")
print(f"Found {len(articles)} div.summary-item")

if articles:
    first = articles[0]
    print(f"\nFirst article HTML (first 300 chars):")
    print(str(first)[:500])
