#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

url = "https://www.wired.com/tag/artificial-intelligence/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, verify=False, timeout=30)
soup = BeautifulSoup(response.text, "lxml")

articles = soup.select("div.summary-item")
print(f"Found {len(articles)} articles")

from ai_news_crawler.config.settings import SourceConfig
from ai_news_crawler.crawlers.bs_crawler import BeautifulSoupCrawler

config = SourceConfig(
    name="Wired - AI",
    url="https://www.wired.com/tag/artificial-intelligence/",
    base_url="https://www.wired.com",
    category="industry",
    enabled=True,
    crawler_type="beautifulsoup",
    article_selector="div.summary-item",
    title_selector="a",
    date_selector="time",
    summary_selector=".summary-item__dek p",
    link_selector="a",
    date_format="%B %d, %Y",
)

crawler = BeautifulSoupCrawler(config)

first = articles[0]
result = crawler._extract_article(first)

print(f"\nExtraction result: {result}")
if result:
    print(f"  Title: {result.title}")
    print(f"  URL: {result.url}")
