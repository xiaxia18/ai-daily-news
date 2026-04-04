#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://juejin.cn/backend/ai"
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

soup = BeautifulSoup(response.text, "lxml")
print(f"\nTitle: {soup.title}")

# Look for article items
articles = soup.select("div.article-item")
print(f"Found {len(articles)} .article-item")

articles = soup.select("a.entry-title")
print(f"Found {len(articles)} a.entry-title")

if len(response.text) < 20000:
    print(f"\nPreview:\n{response.text[:2000]}")
