#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://aijobs.net"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, verify=False, timeout=30)
print(f"Status: {response.status_code}")
print(f"URL: {response.url}")

soup = BeautifulSoup(response.text, "lxml")
jobs = soup.select("article.card")
print(f"Found {len(jobs)} job articles on homepage")
