#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning
from datetime import date, timedelta

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

from ai_news_crawler.crawlers.bs_crawler import BeautifulSoupCrawler
from ai_news_crawler.config.settings import load_sources

# Load sources and find arXiv
sources = load_sources()
arxiv_config = next(s for s in sources if s.name == "arXiv - CS.AI Recent")

crawler = BeautifulSoupCrawler(arxiv_config)
articles = crawler.crawl()

print(f"Total crawled: {len(articles)} articles from arXiv")
print(f"\nAll titles (lowercase):")

# Keywords from filter.py
ai_coding_keywords = [
    "video", "image", "coding", "codec", "compression",
    "av1", "h.264", "h.265", "hevc", "vvc",
    "neural compression", "deep compression",
    "generative coding", "intra coding", "inter coding",
    "transform coding", "image compression", "video compression",
    "visual coding", "computational photography", "computer vision",
    "visual perception", "image generation", "video generation",
    "encoding", "decoding", "codec"
]

matches = []
for i, article in enumerate(articles):
    title_lower = article.title.lower()
    matched = [kw for kw in ai_coding_keywords if kw in title_lower]
    if matched:
        matches.append((article.title, matched, article.summary[:100]))
        print(f"\n{i+1}. {article.title}")
        print(f"   Matched keywords: {matched}")
        if article.summary:
            print(f"   Summary: {article.summary[:100]}...")

print(f"\n=== Summary ===")
print(f"Total articles: {len(articles)}")
print(f"Matching articles (video/image coding related): {len(matches)}")
