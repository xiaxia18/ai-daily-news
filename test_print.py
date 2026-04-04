#!/usr/bin/env python3
"""Test print first article from crawling."""

from ai_news_crawler.config.settings import load_settings, load_sources
from ai_news_crawler.crawlers.base_crawler import BaseCrawler
from ai_news_crawler.crawlers.bs_crawler import BeautifulSoupCrawler
from ai_news_crawler.processors.filter import filter_and_deduplicate


def create_crawler(config):
    if config.crawler_type == "beautifulsoup":
        return BeautifulSoupCrawler(config)


settings = load_settings()
sources = load_sources()
enabled_sources = [s for s in sources if s.enabled]

print(f"Enabled sources: {len(enabled_sources)}")

for source in enabled_sources:
    print(f"\nCrawling {source.name}...")
    crawler = create_crawler(source)
    articles = crawler.crawl()
    filtered = filter_and_deduplicate(articles, 7)
    print(f"Got {len(articles)} articles, filtered: {len(filtered)}")
    if filtered:
        first = filtered[0]
        print(f"\nFirst article:")
        print(f"  Title: {first.title}")
        print(f"  URL: {first.url}")
        print(f"  Source: {first.source_name}")
        print(f"  Category: {first.category}")
        print(f"  Summary: {first.summary}")
