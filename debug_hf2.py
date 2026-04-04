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

body = soup.select_one("body")
print(f"Body length: {len(str(body))}")

jobs = soup.find_all(True, {"class": lambda c: c and "job" in c})
print(f"Found {len(jobs)} elements with 'job' in class")

# Print first 20 classes
classes = set()
for tag in soup.find_all(True):
    if hasattr(tag, 'attrs') and 'class' in tag.attrs:
        for c in tag.attrs['class']:
            classes.add(c)
            if len(classes) > 20:
                break

print(f"\nFirst 20 classes: {list(classes)[:20]}")
