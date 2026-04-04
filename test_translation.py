#!/usr/bin/env python3
"""Test translation without sending email."""

import logging
from typing import List

from ai_news_crawler.config.settings import load_settings, load_sources, SourceConfig
from ai_news_crawler.crawlers.base_crawler import BaseCrawler
from ai_news_crawler.crawlers.bs_crawler import BeautifulSoupCrawler
from ai_news_crawler.models.article import Article
from ai_news_crawler.processors.filter import filter_and_deduplicate, group_by_category

from ai_news_crawler.utils.logging import setup_logging

settings = load_settings()
setup_logging(settings.log_level)

logger = logging.getLogger(__name__)

def create_crawler(config: SourceConfig) -> BaseCrawler:
    if config.crawler_type == "beautifulsoup":
        return BeautifulSoupCrawler(config)
    else:
        raise ValueError(f"Unknown crawler type: {config.crawler_type}")

# Load sources
sources = load_sources()
enabled_sources = [s for s in sources if s.enabled]
logger.info(f"Loaded {len(enabled_sources)} enabled sources")

# Crawl all sources
all_articles: List[Article] = []
for source in enabled_sources:
    logger.info(f"Crawling {source.name}...")
    crawler = create_crawler(source)
    articles = crawler.crawl()
    all_articles.extend(articles)

logger.info(f"Total articles crawled: {len(all_articles)}")

# Filter and deduplicate
filtered = filter_and_deduplicate(all_articles, include_recent_days=1)
logger.info(f"After filtering: {len(filtered)} articles")

# Group by category
by_category = group_by_category(filtered)
logger.info(f"Articles grouped into {len(by_category)} categories")

# Print sample results
print("\n" + "="*80)
print("SAMPLE RESULTS (after translation):")
print("="*80)

for cat, articles in by_category.items():
    print(f"\n== {cat} ==")
    for i, article in enumerate(articles[:3]):
        print(f"\n{i+1}. {article.title}")
        if article.summary:
            summary = article.summary[:150]
            print(f"   {summary}...")
        print(f"   source: {article.source_name}, origin: {article.origin}")

# Count translated vs original
translated_count = 0
for article in filtered:
    if article.origin == "international":
        # Check if title contains Chinese characters
        if any('\u4e00' <= c <= '\u9fff' for c in article.title):
            translated_count += 1

print(f"\nStatistics:")
print(f"  Total filtered articles: {len(filtered)}")
print(f"  International articles: {len([a for a in filtered if a.origin == 'international'])}")
print(f"  Successfully translated: {translated_count}")
