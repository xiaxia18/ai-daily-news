import re
import time
import warnings
from datetime import datetime, date, timedelta
from typing import List, Optional
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup, Tag

# Disable warnings for unverified HTTPS requests
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

from deep_translator import GoogleTranslator

from ai_news_crawler.crawlers.base_crawler import BaseCrawler
from ai_news_crawler.models.article import Article
from ai_news_crawler.config.settings import SourceConfig

logger = logging.getLogger(__name__)


class BeautifulSoupCrawler(BaseCrawler):
    """Crawler using BeautifulSoup for static HTML pages."""

    def __init__(self, config: SourceConfig):
        self.config = config
        self.session = requests.Session()
        # More browser-like headers to avoid anti-crawler blocking
        # Note: no br (brotli) because requests doesn't support it by default
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })
        # Add retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        # Add delay between requests to be polite
        time.sleep(1)

    def crawl(self) -> List[Article]:
        """Crawl the configured URL and extract articles."""
        try:
            response = self.session.get(self.config.url, timeout=30, verify=False)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {self.config.url}: {e}")
            return []

        soup = BeautifulSoup(response.text, "lxml")
        article_elements = soup.select(self.config.article_selector)

        articles = []

        # Special handling for arXiv - title is in next sibling dd
        if self.config.name.startswith("arXiv"):
            # arXiv has dt + dd pairs, iterate through dt elements
            for dt in article_elements:
                if dt.name == "dt":
                    dd = dt.find_next_sibling("dd")
                    article = self._extract_article_arxiv(dt, dd)
                    if article:
                        articles.append(article)
        else:
            for elem in article_elements:
                article = self._extract_article(elem)
                if article:
                    articles.append(article)

        logger.info(f"Crawled {len(articles)} articles from {self.config.name}")
        return articles

    def _extract_article(self, elem: Tag) -> Optional[Article]:
        """Extract article data from a DOM element."""
        # Extract link
        if self.config.link_selector:
            link_elem = elem.select_one(self.config.link_selector)
        else:
            link_elem = elem if elem.name == "a" else elem.find("a")

        if not link_elem or not hasattr(link_elem, "get"):
            return None

        url = link_elem.get(self.config.link_attr)
        if not url:
            url = link_elem.get("href")
        if not url:
            return None

        # Resolve relative URL
        if self.config.needs_resolve_url:
            if url.startswith("/"):
                url = self.config.base_url.rstrip("/") + url
            elif not url.startswith(("http://", "https://")):
                url = self.config.base_url.rstrip("/") + "/" + url

        # Extract title
        title = self._extract_text(elem, self.config.title_selector)
        if not title:
            title = link_elem.get_text(strip=True)
        if not title:
            return None

        # Extract summary from list page
        summary = self._extract_text(elem, self.config.summary_selector)

        # If configured, fetch full article detail page and extract content summary
        if self.config.fetch_full_article and self.config.full_content_selector:
            try:
                time.sleep(0.5)  # be polite
                response = self.session.get(url, timeout=20, verify=False)
                response.raise_for_status()
                detail_soup = BeautifulSoup(response.text, "lxml")
                content_elem = detail_soup.select_one(self.config.full_content_selector)
                if content_elem:
                    # Extract all paragraphs and combine
                    paragraphs = content_elem.select("p")
                    if paragraphs:
                        full_text = " ".join([p.get_text(strip=True) for p in paragraphs[:3]])
                        # Truncate to keep it concise
                        if len(full_text) > 300:
                            full_text = full_text[:297] + "..."
                        summary = full_text
            except requests.RequestException as e:
                logger.warning(f"Failed to fetch full article {url}: {e}")

        # Translate title and summary to Chinese if it's international origin
        if self.config.origin == "international":
            try:
                translator = GoogleTranslator(source='en', target='zh-CN')
                if title and len(title) > 0:
                    title_trans = translator.translate(title[:500])  # Limit length
                    if title_trans:
                        title = title_trans
                if summary and len(summary) > 0:
                    # Translate in chunks to avoid API limits
                    if len(summary) > 500:
                        summary = summary[:500]
                    summary_trans = translator.translate(summary)
                    if summary_trans:
                        summary = summary_trans
                time.sleep(0.3)  # Rate limiting
            except Exception as e:
                logger.warning(f"Failed to translate article {title}: {e}")

        # Extract date
        published_date = self._extract_date(elem, self.config.date_selector)

        return Article(
            title=title.strip(),
            url=url,
            source_name=self.config.name,
            category=self.config.category,
            origin=self.config.origin,
            summary=summary.strip() if summary else None,
            published_date=published_date,
        )

    def _extract_text(self, elem: Tag, selector: Optional[str]) -> str:
        """Extract text using a CSS selector."""
        if not selector:
            return ""
        selected = elem.select_one(selector)
        if selected:
            return selected.get_text(strip=True)
        return ""

    def _extract_article_arxiv(self, dt: Tag, dd: Tag) -> Optional[Article]:
        """Special extraction for arXiv where title is in dd."""
        # Extract link from dt
        if self.config.link_selector:
            link_elem = dt.select_one(self.config.link_selector)
        else:
            link_elem = dt if dt.name == "a" else dt.find("a")

        if not link_elem or not hasattr(link_elem, "get"):
            return None

        url = link_elem.get("href")
        if not url:
            return None

        # Resolve relative URL
        if self.config.needs_resolve_url:
            if url.startswith("/"):
                url = self.config.base_url.rstrip("/") + url
            elif not url.startswith(("http://", "https://")):
                url = self.config.base_url.rstrip("/") + "/" + url

        # Extract title from dd
        title = ""
        if dd:
            title_elem = dd.select_one(".list-title")
            if title_elem:
                title = title_elem.get_text(strip=True)
                # Remove "Title:" prefix
                title = title.replace("Title:", "").strip()
                # arXiv adds a trailing dot, remove it
                title = title.rstrip('.')

        if not title:
            return None

        # Extract abstract/summary
        summary = ""
        if dd:
            abstract_elem = dd.select_one(".abstract")
            if abstract_elem:
                summary = abstract_elem.get_text(strip=True)
                summary = summary.replace("Abstract:", "").strip()
                # Truncate to keep it concise
                if len(summary) > 300:
                    summary = summary[:297] + "..."

        # arXiv doesn't have publication date on list page
        return Article(
            title=title.strip(),
            url=url,
            source_name=self.config.name,
            category=self.config.category,
            origin=self.config.origin,
            summary=summary,
            published_date=None,
        )

    def _extract_date(self, elem: Tag, selector: Optional[str]) -> Optional[date]:
        """Extract and parse published date."""
        if not selector:
            return None

        date_text = self._extract_text(elem, selector)
        if not date_text:
            return None

        # Clean up date text
        date_text = re.sub(r"[^\w\s/-]", "", date_text)
        date_text_lower = date_text.lower()

        # Handle relative dates (Chinese: 今天, 昨天)
        today = date.today()
        if '今天' in date_text or '今日' in date_text:
            return today
        if '昨天' in date_text or '昨日' in date_text:
            return today - timedelta(days=1)
        if '前天' in date_text:
            return today - timedelta(days=2)

        try:
            parsed = datetime.strptime(date_text, self.config.date_format)
            return parsed.date()
        except ValueError:
            # Try some common formats
            for fmt in ["%B %d, %Y", "%b %d, %Y", "%Y-%m-%d", "%d %B %Y", "%m/%d/%Y"]:
                try:
                    parsed = datetime.strptime(date_text, fmt)
                    return parsed.date()
                except ValueError:
                    continue
            logger.warning(f"Could not parse date '{date_text}' for {self.config.name}")
            return None
