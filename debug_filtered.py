#!/usr/bin/env python3
"""Debug why jobs don't appear in output."""

import logging
from ai_news_crawler.config.settings import load_settings, load_sources, SourceConfig
from ai_news_crawler.crawlers.base_crawler import BaseCrawler
from ai_news_crawler.crawlers.bs_crawler import BeautifulSoupCrawler
from ai_news_crawler.crawlers.selenium_crawler import SeleniumCrawler
from ai_news_crawler.models.article import Article
from ai_news_crawler.processors.filter import filter_and_deduplicate, group_by_category

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_crawler(config: SourceConfig) -> BaseCrawler:
    if config.crawler_type == "beautifulsoup":
        return BeautifulSoupCrawler(config)
    elif config.crawler_type == "selenium":
        return SeleniumCrawler(config)
    else:
        raise ValueError(f"Unknown crawler type: {config.crawler_type}")

def main():
    settings = load_settings()

    sources = load_sources()
    enabled_sources = [s for s in sources if s.enabled]
    logger.info(f"Loaded {len(enabled_sources)} enabled sources")

    all_articles = []
    for source in enabled_sources:
        logger.info(f"Crawling {source.name}...")
        crawler = create_crawler(source)
        articles = crawler.crawl()
        all_articles.extend(articles)
        logger.info(f"  -> {len(articles)} articles from {source.name}")

    logger.info(f"Total articles crawled: {len(all_articles)}")

    # Count by category
    from collections import Counter
    cat_counter = Counter()
    for art in all_articles:
        cat_counter[art.category] += 1
    logger.info(f"By category before filtering: {dict(cat_counter)}")

    filtered = filter_and_deduplicate(all_articles, include_recent_days=1)
    logger.info(f"After filtering: {len(filtered)} articles")

    cat_counter2 = Counter()
    for art in filtered:
        cat_counter2[art.category] += 1
    logger.info(f"By category after filtering: {dict(cat_counter2)}")

    by_category = group_by_category(filtered)
    logger.info(f"Groups after grouping: {list(by_category.keys())}")

    # Print jobs
    if 'jobs' in by_category:
        logger.info(f"Jobs in final: {len(by_category['jobs'])} jobs")
        for i, job in enumerate(by_category['jobs']):
            logger.info(f"  {i+1}. {job.title} -> {job.url}")

if __name__ == "__main__":
    main()
