#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://huggingface.co/jobs"
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

# Look for any article elements
all_articles = soup.find_all("article")
print(f"\nFound {len(all_articles)} article tags total")

# Look for job items
for tag in soup.find_all(True):
    if 'class' in tag.attrs:
        classes = tag.attrs['class']
        classes_str = ' '.join(classes).lower()
        if 'job' in classes_str:
            print(f"\n  Found: {tag.name} .{'.'.join(classes)}")

# Check if it's server rendered
body = soup.find("body")
if body:
    print(f"\nBody has {len(body.contents)} children")
    # Check how much content we have
    text = soup.get_text()
    print(f"Total text length: {len(text)}")
    print(f"\nText preview (first 1000 chars):\n{text[:1000]}")
