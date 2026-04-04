# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Overview

This is **AI Daily News Crawler & Briefing** - a Python application that crawls AI news websites daily, aggregates articles by category (industry news, academic papers, technology updates, AI jobs), and sends a formatted briefing via email using GitHub Actions for scheduling.

## Commands

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run manually (development/testing)
```bash
python main.py
```

## Project Structure

```
ai_news_crawler/
├── config/
│   ├── settings.py       # Configuration loader (pydantic + env)
│   └── sources.yaml      # Crawler source definitions (edit me to add sources)
├── crawlers/
│   ├── base_crawler.py   # Abstract base crawler
│   └── bs_crawler.py     # BeautifulSoup crawler implementation
├── models/
│   └── article.py        # Article dataclass model
├── processors/
│   ├── filter.py         # Filtering/deduplication/grouping
│   └── formatter.py      # Briefing formatting
├── email/
│   ├── sender.py         # Email sending via SMTP
│   └── templates/
│       └── daily_briefing.html.j2  # Jinja2 HTML template
└── utils/
    └── logging.py        # Logging setup

.github/workflows/
└── daily-crawl.yml       # GitHub Actions daily workflow
```

## Key Architecture

- **Configuration-driven**: All sources are defined in `sources.yaml`. Adding new sources doesn't require code changes.
- **Categorized output**: Articles are grouped into 4 categories. Each source specifies its category in YAML.
- **Scheduling**: GitHub Actions runs daily at 8 AM UTC (free hosted, no server needed).
- **BeautifulSoup**: Uses simple requests + BeautifulSoup for static sites. Add Selenium later if dynamic content is needed.
- **Email**: Sends formatted HTML email via SMTP. Credentials stored in GitHub Secrets.

## Categories

- `industry` - AI Industry News
- `academic` - AI Academic Papers
- `technology` - AI Technology & Engineering
- `jobs` - AI Jobs & Careers

When adding new sources, assign to one of these categories.

## Development Notes

- Always test crawler after adding a new source: `python main.py`
- Check that CSS selectors correctly extract articles by looking at the page source in browser DevTools
- The crawler respects `enabled: false` in sources.yaml - you can disable broken sources without deleting them
- GitHub Actions workflow includes failure notification - you'll get an email if the crawl fails

## Current Status & Special Features

- **Industry News**: Enabled sources - Wired (English), 开源中国 (Chinese AI news)
- **Academic Papers**: arXiv CS.AI - automatically filters for video/image coding related papers, limited to max 3 papers in output
- **Chinese relative date support**: 支持 "今天", "昨天", "前天" 相对日期解析
- **Custom link attribute**: Supports `link_attr` config for extracting URL from `data-url` etc.
- **Jobs category**: Framework ready, but most Chinese job sites require JS rendering and have anti-crawler protection. Add a working static source in `sources.yaml` when found.

## Filtering Rules

- Industry news: keep only articles from today
- Academic papers: keep only papers with video/image coding keywords, max 3
- Jobs: keep only jobs posted in last 7 days
- All categories: deduplicated by URL
