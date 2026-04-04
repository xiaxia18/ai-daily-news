#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://ai.googleblog.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, verify=False, timeout=30)
soup = BeautifulSoup(response.text, "lxml")

articles = soup.select(".post")
print(f"Found {len(articles)} articles with .post")

articles = soup.select("div.entry")
print(f"Found {len(articles)} articles with div.entry")

if articles:
    first = articles[0]
    print(f"\nFirst article HTML (first 300 chars):")
    print(str(first)[:500])
