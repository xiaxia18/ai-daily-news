#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://www.huxiu.com/tag/121.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

response = requests.get(url, verify=False, timeout=30, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

# Find any article
for tag in soup.find_all(["div"]):
    if 'class' in tag.attrs:
        classes = ' '.join(tag.attrs['class']).lower()
        if 'article' in classes or 'item' in classes:
            print(f"{tag.name}: {classes}")

# Get the whole content preview
print(f"\nPreview first 1500 chars:")
print(response.text[:1500])
