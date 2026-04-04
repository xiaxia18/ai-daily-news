#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://aijobs.net"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

response = requests.get(url, verify=False, timeout=30, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

job_links = soup.select("a[href^='/job/']")
if job_links:
    # Go up to find the containing row
    current = job_links[0]
    for _ in range(5):
        print(f"Level {_}: {current.name} {current.get('class')}")
        parent = current.parent
        if parent is None:
            break
        current = parent

# Print the full html starting from body
body = soup.body
if body:
    print(f"\nBody structure first 1500 chars:")
    print(str(body)[:1500])
