#!/usr/bin/env python3
"""Main entry point for AI Daily News Crawler."""

import logging
from typing import List

from ai_news_crawler.config.settings import load_settings, load_sources, SourceConfig
from ai_news_crawler.crawlers.base_crawler import BaseCrawler
from ai_news_crawler.crawlers.bs_crawler import BeautifulSoupCrawler
from ai_news_crawler.crawlers.selenium_crawler import SeleniumCrawler
from ai_news_crawler.models.article import Article
from ai_news_crawler.processors.filter import filter_and_deduplicate, group_by_category
from ai_news_crawler.email.sender import compile_and_send
from ai_news_crawler.utils.logging import setup_logging

logger = logging.getLogger(__name__)


def create_crawler(config: SourceConfig) -> BaseCrawler:
    """Factory method to create crawler based on configuration."""
    if config.crawler_type == "beautifulsoup":
        return BeautifulSoupCrawler(config)
    elif config.crawler_type == "selenium":
        return SeleniumCrawler(config)
    else:
        raise ValueError(f"Unknown crawler type: {config.crawler_type}")


def run_crawler() -> None:
    """Run the full crawling process."""
    settings = load_settings()
    setup_logging(settings.log_level)

    logger.info("Starting AI Daily News Crawler")

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

    # Filter and deduplicate - only include today/recent 1 day
    filtered = filter_and_deduplicate(all_articles, include_recent_days=1)
    logger.info(f"After filtering: {len(filtered)} articles")

    if not filtered:
        logger.warning("No articles found after filtering. Trying last 3 days...")
        filtered = filter_and_deduplicate(all_articles, include_recent_days=3)

    # Group by category
    by_category = group_by_category(filtered)
    logger.info(f"Articles grouped into {len(by_category)} categories")

    # Send email
    if settings.send_email:
        success = compile_and_send(by_category, settings)
        if success:
            logger.info("Done! Email sent.")
        else:
            logger.error("Failed to send email")
    else:
        logger.info("Email sending disabled. Done.")


if __name__ == "__main__":
    run_crawler()
