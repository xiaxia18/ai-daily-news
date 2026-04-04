import os
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import yaml

from ai_news_crawler.models.article import Article


class SourceConfig(BaseModel):
    """Configuration for a single crawler source."""
    name: str
    url: str
    base_url: str
    category: str
    origin: str = "international"  # "domestic" or "international"
    company: Optional[str] = None  # For jobs: company name (byteDance, alibaba, tencent, baidu, etc)
    enabled: bool = True
    crawler_type: str = "beautifulsoup"
    article_selector: str
    title_selector: Optional[str] = None
    date_selector: Optional[str] = None
    summary_selector: Optional[str] = None
    link_selector: Optional[str] = None
    link_attr: str = "href"
    date_format: str = "%Y-%m-%d"
    needs_resolve_url: bool = True
    fetch_full_article: bool = False  # Whether to fetch detail page for full content
    full_content_selector: Optional[str] = None  # Selector for article content on detail page


class Settings(BaseModel):
    """Application settings loaded from environment variables."""
    smtp_server: str
    smtp_port: int = 587
    smtp_username: str
    smtp_password: str
    recipient_email: str
    log_level: str = "INFO"
    max_articles_per_category: int = 15
    send_email: bool = True


def load_settings() -> Settings:
    """Load settings from environment variables."""
    load_dotenv()
    return Settings(
        smtp_server=os.getenv("SMTP_SERVER"),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_username=os.getenv("SMTP_USERNAME"),
        smtp_password=os.getenv("SMTP_PASSWORD"),
        recipient_email=os.getenv("RECIPIENT_EMAIL"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        max_articles_per_category=int(os.getenv("MAX_ARTICLES_PER_CATEGORY", "15")),
        send_email=os.getenv("SEND_EMAIL", "true").lower() == "true",
    )


def load_sources(config_path: str = "ai_news_crawler/config/sources.yaml") -> List[SourceConfig]:
    """Load source configurations from YAML file."""
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [SourceConfig(**source) for source in data["sources"]]
