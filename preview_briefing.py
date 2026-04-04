#!/usr/bin/env python3
"""Generate a preview HTML file of the briefing to verify content is correct."""

import logging
from typing import List

from ai_news_crawler.config.settings import load_settings, load_sources, SourceConfig
from ai_news_crawler.crawlers.base_crawler import BaseCrawler
from ai_news_crawler.crawlers.bs_crawler import BeautifulSoupCrawler
from ai_news_crawler.crawlers.selenium_crawler import SeleniumCrawler
from ai_news_crawler.models.article import Article
from ai_news_crawler.processors.filter import filter_and_deduplicate, group_by_category
from ai_news_crawler.processors.formatter import format_briefing
from ai_news_crawler.email.sender import render_briefing

from ai_news_crawler.utils.logging import setup_logging

settings = load_settings()
setup_logging(settings.log_level)

logger = logging.getLogger(__name__)

def create_crawler(config: SourceConfig) -> BaseCrawler:
    if config.crawler_type == "beautifulsoup":
        return BeautifulSoupCrawler(config)
    elif config.crawler_type == "selenium":
        return SeleniumCrawler(config)
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

# Format and render
context = format_briefing(by_category, settings)
html = render_briefing(context)

# Save to file
output_file = "preview_briefing.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n=== Preview generated ===")
print(f"Output file: {output_file}")
print(f"Categories in output: {len(context['categories'])}")
for cat in context['categories']:
    print(f"  - {cat['name']}: {len(cat['articles'])} articles")
