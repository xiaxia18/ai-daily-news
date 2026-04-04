from collections import OrderedDict
from typing import List, Dict
from datetime import date, timedelta

from ai_news_crawler.models.article import Article


def filter_and_deduplicate(articles: List[Article], include_recent_days: int = 1) -> List[Article]:
    """Filter articles by date and remove duplicates based on URL.

    If no articles fall within the date range, return the most recent articles
    to ensure we always have content for the briefing.

    For arXiv academic papers, filter to only keep video/image coding related papers.
    For job postings, filter to only keep last 7 days.

    Args:
        articles: List of crawled articles
        include_recent_days: Include articles from last N days (1=today only)

    Returns:
        Filtered and deduplicated list of articles
    """
    # Deduplicate using OrderedDict to preserve order
    unique_articles = list(OrderedDict.fromkeys(articles))

    # Different date cutoff for different categories
    filtered = []
    for article in unique_articles:
        if article.category == "jobs":
            # Jobs: keep last 7 days
            cutoff = date.today() - timedelta(days=7)
            if article.published_date is None:
                filtered.append(article)
            elif article.published_date >= cutoff:
                filtered.append(article)
        elif article.category == "academic":
            # Academic papers: keep last 7 days (arXiv doesn't have date on list page,
            # so keep all since they are already the most recent submissions
            cutoff = date.today() - timedelta(days=7)
            if article.published_date is None:
                filtered.append(article)
            elif article.published_date >= cutoff:
                filtered.append(article)
        else:
            # Industry news:
            # - domestic (Chinese): keep last 3 days to ensure we always have content
            # - international: keep last 1 day (today only)
            if article.origin == "domestic":
                cutoff = date.today() - timedelta(days=3)
            else:
                cutoff = date.today() - timedelta(days=include_recent_days - 1)
            if article.published_date is None:
                filtered.append(article)
            elif article.published_date >= cutoff:
                filtered.append(article)

    # If no articles in date range, try 3 days for non-jobs
    if not filtered:
        cutoff = date.today() - timedelta(days=2)
        for article in unique_articles:
            if article.category == "jobs":
                continue
            if article.published_date is None:
                filtered.append(article)
            elif article.published_date >= cutoff:
                filtered.append(article)

    # Special filtering for arXiv academic papers: only keep video/image coding related
    ai_coding_keywords = [
        "video", "image", "coding", "codec", "compression",
        "av1", "h.264", "h.265", "hevc", "vvc",
        "neural compression", "deep compression",
        "generative coding", "intra coding", "inter coding",
        "transform coding", "image compression", "video compression",
        "visual coding", "computational photography", "computer vision",
        "visual perception", "image generation", "video generation",
        "encoding", "decoding", "codec"
    ]

    # Check if we have arXiv articles and filter them
    has_arxiv = any(article.source_name.startswith("arXiv") for article in filtered)
    if has_arxiv:
        filtered_arxiv = []
        arxiv_matched = []
        arxiv_other = []
        for article in filtered:
            if article.source_name.startswith("arXiv"):
                title_lower = article.title.lower()
                # Check if any keyword matches
                if any(keyword in title_lower for keyword in ai_coding_keywords):
                    arxiv_matched.append(article)
                else:
                    arxiv_other.append(article)
            else:
                filtered_arxiv.append(article)

        # If we have keyword matches, use them
        if arxiv_matched:
            filtered_arxiv.extend(arxiv_matched)
            filtered = filtered_arxiv
        # If no matches but we have other arXiv papers, add up to 3 recent ones
        elif arxiv_other:
            filtered_arxiv.extend(arxiv_other[:3])
            filtered = filtered_arxiv
        # If we have anything left, keep it
        if filtered_arxiv:
            filtered = filtered_arxiv

    # If still no articles in date range, return the most recent 10 articles
    if not filtered and unique_articles:
        # Sort by date descending and take most recent
        sorted_articles = sorted(
            unique_articles,
            key=lambda a: a.published_date if a.published_date else date.min,
            reverse=True
        )
        filtered = sorted_articles[:10]

    return filtered


def group_by_category(articles: List[Article]) -> Dict[str, List[Article]]:
    """Group articles by category."""
    categories: Dict[str, List[Article]] = {}
    for article in articles:
        cat = article.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(article)
    return categories
