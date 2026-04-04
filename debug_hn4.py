#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://news.ycombinator.com/submitted?id=whoishiring"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, verify=False, timeout=30)
soup = BeautifulSoup(response.text, "lxml")

things = soup.select("tr.athing")
first = things[0]

print("First tr.athing content:")
print(first.prettify()[:500])
