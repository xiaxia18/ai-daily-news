#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://huggingface.co/jobs"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, verify=False, timeout=30)
soup = BeautifulSoup(response.text, "lxml")

articles = soup.select("article.border-border")
print(f"Found {len(articles)} articles with .border-border")

articles = soup.select("article")
print(f"Found {len(articles)} articles total")

if articles:
    first = articles[0]
    print("\nFirst article HTML:")
    print(first.prettify()[:500])
