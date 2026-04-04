#!/usr/bin/env python3
"""Generate preview HTML without sending email."""

import logging
from ai_news_crawler.config.settings import load_settings, load_sources, SourceConfig
from ai_news_crawler.crawlers.base_crawler import BaseCrawler
from ai_news_crawler.crawlers.bs_crawler import BeautifulSoupCrawler
from ai_news_crawler.crawlers.selenium_crawler import SeleniumCrawler
from ai_news_crawler.models.article import Article
from ai_news_crawler.processors.filter import filter_and_deduplicate, group_by_category
from ai_news_crawler.processors.formatter import format_briefing
from jinja2 import Environment, FileSystemLoader
import os

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

    logger.info(f"Total articles crawled: {len(all_articles)}")

    filtered = filter_and_deduplicate(all_articles, include_recent_days=1)
    logger.info(f"After filtering: {len(filtered)} articles")

    from collections import Counter
    cat_counter = Counter()
    for art in filtered:
        cat_counter[art.category] += 1
    logger.info(f"By category after filtering: {dict(cat_counter)}")

    by_category = group_by_category(filtered)
    logger.info(f"Groups after grouping: {list(by_category.keys())}")

    # Format briefing
    context = format_briefing(by_category, settings)

    # Load template and render
    template_dir = os.path.join(os.path.dirname(__file__), 'ai_news_crawler', 'email', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('daily_briefing.html.j2')
    html_output = template.render(context)

    # Save to preview file
    with open('preview_briefing.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

    logger.info(f"Preview saved to preview_briefing.html")
    logger.info(f"Total categories in output: {len(context['categories'])}")
    for i, cat in enumerate(context['categories']):
        if cat.get('is_company_section'):
            logger.info(f"  {i+1}. {cat['name']} (company section): {len(cat['articles'])} jobs")
        else:
            logger.info(f"  {i+1}. {cat['name']}: {len(cat['articles'])} articles")

if __name__ == "__main__":
    main()
