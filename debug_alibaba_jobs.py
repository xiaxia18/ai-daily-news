#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://job.alibaba.com/zhaopin/positionList.htm"
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
print(f"Title: {soup.title}")

# Count divs
all_divs = soup.find_all("div")
print(f"Total divs: {len(all_divs)}")

# Check body content
body = soup.body
if body:
    print(f"Body children: {len(body.contents)}")
    for i, child in enumerate(body.contents[:5]):
        if hasattr(child, 'name'):
            print(f"  {i}: {child.name}")
