#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning
import re

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

scripts = soup.find_all("script")
print(f"Found {len(scripts)} scripts")

# Look for script that has job data
for i, script in enumerate(scripts):
    if script.string and "jobs" in script.string:
        lines = script.string.splitlines()
        print(f"\nScript {i} has 'jobs', first 5 lines:")
        print('\n'.join(lines[:5]))
        break
