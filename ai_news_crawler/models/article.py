from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Article:
    """Represents a crawled news article."""
    title: str
    url: str
    source_name: str
    category: str
    origin: str = "international"  # "domestic" or "international"
    summary: Optional[str] = None
    published_date: Optional[date] = None
    author: Optional[str] = None

    @property
    def is_today(self) -> bool:
        """Check if article was published today."""
        if self.published_date is None:
            return True
        return self.published_date == date.today()

    def __hash__(self) -> int:
        """Hash based on URL for deduplication."""
        return hash(self.url)

    def __eq__(self, other) -> bool:
        """Equality based on URL for deduplication."""
        if not isinstance(other, Article):
            return False
        return self.url == other.url
