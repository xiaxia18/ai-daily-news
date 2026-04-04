from typing import Dict, List
from datetime import date

from ai_news_crawler.models.article import Article
from ai_news_crawler.config.settings import Settings


CATEGORY_NAMES = {
    "industry_domestic": "AI 行业资讯 - 国内",
    "industry_international": "AI 行业资讯 - 国际",
    "academic": "AI 学术论文 - 图像视频编解码",
    "technology": "AI 技术工程",
    "jobs": "AI 招聘信息",
}


def format_briefing(articles_by_category: Dict[str, List[Article]], settings: Settings) -> Dict:
    """Format the briefing HTML from categorized articles."""

    today = date.today().strftime("%Y年%m月%d日 %A")
    total_articles = sum(len(articles) for articles in articles_by_category.values())

    # Sort articles within each category and limit
    limited_by_category: Dict[str, List[Article]] = {}

    for cat, articles in articles_by_category.items():
        # Sort by date (newest first)
        sorted_articles = sorted(
            articles,
            key=lambda a: a.published_date if a.published_date else date.min,
            reverse=True
        )

        if cat == "industry":
            # Split into domestic and international, limit to 5 each
            domestic = [a for a in sorted_articles if a.origin == "domestic"]
            international = [a for a in sorted_articles if a.origin != "domestic"]
            limited_by_category["industry_domestic"] = domestic[:5]
            limited_by_category["industry_international"] = international[:5]
        elif cat == "academic":
            # Special limit: max 3 papers for academic category
            limited_by_category[cat] = sorted_articles[:3]
        elif cat == "jobs":
            # Group by company (source_name = company name), max 3 jobs per company
            from collections import defaultdict
            jobs_by_company = defaultdict(list)
            for job in sorted_articles:
                company = job.source_name
                if len(jobs_by_company[company]) < 3:
                    jobs_by_company[company].append(job)
            limited_by_category[cat] = sorted_articles
            # We'll expand to company groups below
        else:
            limited_by_category[cat] = sorted_articles[:settings.max_articles_per_category]

    # Build final categories
    final_categories = []
    for cat, arts in limited_by_category.items():
        if cat == "jobs":
            # Expand jobs by company
            from collections import defaultdict
            jobs_by_company = defaultdict(list)
            for job in arts:
                company = job.source_name
                if len(jobs_by_company[company]) < 3:  # max 3 per company
                    jobs_by_company[company].append(job)
            # Add each company as a separate section under jobs category
            for company_name, company_jobs in jobs_by_company.items():
                final_categories.append({
                    "name": f"{company_name}",
                    "slug": "jobs",
                    "is_company_section": True,
                    "articles": [
                        {
                            "title": art.title,
                            "url": art.url,
                            "summary": art.summary,
                            "source": art.source_name,
                            "date": "最近" if art.published_date is None else art.published_date.strftime("%m-%d"),
                        }
                        for art in company_jobs
                    ]
                })
        else:
            final_categories.append({
                "name": CATEGORY_NAMES.get(cat, cat),
                "slug": cat,
                "is_company_section": False,
                "articles": [
                    {
                        "title": art.title,
                        "url": art.url,
                        "summary": art.summary,
                        "source": art.source_name,
                        "date": "最近" if art.published_date is None else art.published_date.strftime("%m-%d"),
                    }
                    for art in arts
                ]
            })

    return {
        "date": today,
        "total_articles": total_articles,
        "categories": final_categories
    }
