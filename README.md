# AI Daily News Crawler & Briefing

A Python web crawler that collects the latest AI news from multiple sources every day, categorizes it, and sends a formatted briefing via email.

## Features

- **Multi-category aggregation**:
  - AI Industry News
  - AI Academic Papers
  - AI Technology & Engineering
  - AI Jobs & Career Opportunities
- **Configuration-driven**: Add new sources by editing a YAML file, no code changes required
- **Automatic daily scheduling** via GitHub Actions (free hosting)
- **Deduplication** and date filtering to only include recent articles
- **Clean HTML email format** with categorized sections

## Current Sources

### Industry News
- MIT Technology Review - AI
- VentureBeat - AI
- Wired - AI
- TechCrunch - AI
- KDnuggets
- OpenAI Blog

### Academic Papers
- arXiv - CS.AI Recent Submissions
- Google AI Blog
- Meta AI Blog

### Technology & Engineering
- The Batch (DeepLearning.AI)
- Microsoft AI Blog

### Jobs & Careers
- Hugging Face Jobs
- AI-Jobs.net

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd my_blog
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and fill in your SMTP credentials:

```bash
cp .env.example .env
# Edit .env with your settings
```

Required environment variables:
- `SMTP_SERVER` - SMTP server (e.g., `smtp.gmail.com` for Gmail)
- `SMTP_PORT` - SMTP port (usually 587)
- `SMTP_USERNAME` - SMTP username (your email)
- `SMTP_PASSWORD` - SMTP password (app password for Gmail)
- `RECIPIENT_EMAIL` - Where to send the briefing (can be multiple, comma-separated)

### 4. Run manually for testing

```bash
python main.py
```

### 5. Set up GitHub Secrets

If using GitHub Actions for daily scheduling, add these secrets in your GitHub repository settings:

- `SMTP_SERVER`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `RECIPIENT_EMAIL`

The workflow is configured to run daily at 8:00 AM UTC. You can manually trigger it from the Actions tab.

## Adding New Sources

Edit `ai_news_crawler/config/sources.yaml` and add a new entry:

```yaml
- name: "Source Name"
  url: "https://example.com/ai"
  base_url: "https://example.com"
  category: "industry"  # one of: industry, academic, technology, jobs
  enabled: true
  crawler_type: "beautifulsoup"
  article_selector: ".article"      # CSS selector for article container
  title_selector: ".title a"        # CSS selector for title
  date_selector: ".date"            # CSS selector for published date
  summary_selector: ".summary"      # CSS selector for summary
  link_selector: ".title a"         # CSS selector for link
  date_format: "%B %d, %Y"          # Date format
```

## Requirements

- Python 3.9+
- Working SMTP account for sending emails

## License

MIT
