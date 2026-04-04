from abc import ABC, abstractmethod
from typing import List

from ai_news_crawler.models.article import Article


class BaseCrawler(ABC):
    """Abstract base class for crawlers."""

    @abstractmethod
    def crawl(self) -> List[Article]:
        """Crawl the source and return a list of articles."""
        pass
