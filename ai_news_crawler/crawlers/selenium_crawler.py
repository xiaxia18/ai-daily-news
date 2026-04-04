import time
import re
import logging
from datetime import date
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from ai_news_crawler.crawlers.base_crawler import BaseCrawler
from ai_news_crawler.models.article import Article
from ai_news_crawler.config.settings import SourceConfig

logger = logging.getLogger(__name__)


class SeleniumCrawler(BaseCrawler):
    """Selenium crawler for JavaScript rendered job pages from company career sites."""

    def __init__(self, config: SourceConfig):
        self.config = config
        # Setup Chrome options for headless browsing
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless=new")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument(f"--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    def crawl(self) -> List[Article]:
        """Crawl using Selenium for JavaScript rendered content."""
        driver = None
        try:
            driver = webdriver.Chrome(options=self.chrome_options)
            driver.get(self.config.url)

            # Wait longer for job list to load (especially for ByteDance which is heavy SPA)
            time.sleep(15)

            # Scroll multiple times to trigger lazy loading
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

            # Get page source after rendering
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")

            article_elements = soup.select(self.config.article_selector)
            logger.info(f"Found {len(article_elements)} job items after JS rendering for {self.config.name}")

            articles = []
            for elem in article_elements:
                article = self._extract_job(elem)
                if article:
                    articles.append(article)

            logger.info(f"Crawled {len(articles)} jobs from {self.config.name}")
            return articles

        except Exception as e:
            logger.error(f"Selenium crawl failed for {self.config.url}: {e}")
            return []
        finally:
            if driver:
                driver.quit()

    def _extract_job(self, elem) -> Optional[Article]:
        """Extract job information from a DOM element."""
        # Extract link
        if self.config.link_selector:
            link_elem = elem.select_one(self.config.link_selector)
        else:
            link_elem = elem if elem.name == "a" else elem.find("a")

        # For job sites like Tencent and ByteDance that need special URL construction,
        # if no a tag found, use the whole element for regex searching
        if not link_elem and self.config.category == "jobs":
            link_elem = elem

        if not link_elem or not hasattr(link_elem, "get"):
            return None

        url = link_elem.get(self.config.link_attr)
        if not url:
            url = link_elem.get("href")
        # Special case for Tencent: no href in link, get postId from title and construct URL
        if not url and "腾讯" in self.config.name:
            title = self._extract_text(elem, self.config.title_selector)
            if title:
                # Try to find postId at the end of title (like "AI Research Scientist 107209")
                match = re.search(r' (\d+)$', title.strip())
                if match:
                    post_id = match.group(1)
                    url = f"https://careers.tencent.com/jobdesc.html?postId={post_id}"
        # Special case for ByteDance: no href, get jobId from subtitle and construct URL
        if not url and "字节跳动" in self.config.name:
            # Look for "职位 ID：A58211A" in the subtitle
            all_text = elem.get_text(strip=False)
            if all_text:
                match = re.search(r'职位\s*ID[：:]\s*([A-Za-z0-9]+)', all_text)
                if match:
                    job_id = match.group(1)
                    url = f"https://jobs.bytedance.com/experienced/position/{job_id}"
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

        # Extract summary/job description
        summary = self._extract_text(elem, self.config.summary_selector)

        # Date is usually not available on list page for company career sites
        published_date = None

        return Article(
            title=title.strip(),
            url=url,
            source_name=self.config.name,
            category=self.config.category,
            origin=self.config.origin,
            summary=summary.strip() if summary else None,
            published_date=published_date,
        )

    def _extract_text(self, elem, selector: Optional[str]) -> str:
        """Extract text using a CSS selector."""
        if not selector:
            return ""
        selected = elem.select_one(selector)
        if selected:
            return selected.get_text(strip=True)
        return ""
