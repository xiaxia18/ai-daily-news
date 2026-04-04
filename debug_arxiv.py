#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://arxiv.org/list/cs.AI/recent"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, verify=False, timeout=30)
soup = BeautifulSoup(response.text, "lxml")

articles = soup.select("dt")
print(f"Found {len(articles)} dt elements")

first = articles[0]
print("\nFirst dt HTML:")
print(first.prettify())
print("\n---")

list_title = first.select_one(".list-title")
if list_title:
    print(f"\n.list-title text: '{list_title.get_text(strip=True)}'")

list_identifier = first.select_one(".list-identifier")
if list_identifier:
    print(f"\n.list-identifier text: '{list_identifier.get_text(strip=True)}'")
