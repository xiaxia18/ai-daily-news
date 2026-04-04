#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# Get the list page
url = "https://www.wired.com/tag/artificial-intelligence/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

response = requests.get(url, verify=False, timeout=30, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

# Get first article link
items = soup.select("div.summary-item a")
if items:
    first_link = items[0]
    detail_url = first_link.get("href")
    if not detail_url.startswith("http"):
        detail_url = "https://www.wired.com" + detail_url
    print(f"Fetching: {detail_url}")

    response = requests.get(detail_url, verify=False, timeout=30, headers=headers)
    detail_soup = BeautifulSoup(response.text, "lxml")

    # Find content container
    print(f"\nLooking for content...")
    for selector in [
        "divarticle-content",
        "div.content-body",
        "article div",
        ".article-body",
        "main div",
    ]:
        items = detail_soup.select(selector)
        if items:
            print(f"  {selector}: {len(items)} items")

    print(f"\nFirst 1000 chars of body:")
    main = detail_soup.find("main")
    if main:
        print(main.get_text()[:1000])
