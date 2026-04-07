import sys
import logging
import smtplib
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader

from ai_news_crawler.config.settings import Settings
from ai_news_crawler.processors.formatter import format_briefing
from ai_news_crawler.models.article import Article
from typing import Dict, List

logger = logging.getLogger(__name__)


def render_briefing(context: Dict, template_path: str = "ai_news_crawler/email/templates") -> str:
    """Render the briefing using Jinja2 template."""
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("daily_briefing.html.j2")
    return template.render(**context)


def compile_and_send(articles_by_category: Dict[str, List[Article]], settings: Settings) -> bool:
    """Compile articles into briefing and send email."""
    context = format_briefing(articles_by_category, settings)
    html = render_briefing(context)

    # Clean everything: replace ALL non-breaking spaces with regular spaces
    html = html.replace('\xa0', ' ')
    html = html.replace(u'\xa0', ' ')

    # Use EmailMessage API which handles UTF-8 properly in Python 3
    msg = EmailMessage()
    msg['Subject'] = f"AI 每日简报 - {context['date']}"
    msg['From'] = settings.smtp_username
    msg['To'] = settings.recipient_email

    # Set content with explicit UTF-8 charset - this handles all encoding automatically
    msg.set_content(html, subtype='html', charset='utf-8')

    try:
        if settings.smtp_port == 465:
            # SSL connection
            server = smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port, timeout=60)
        else:
            # STARTTLS
            server = smtplib.SMTP(settings.smtp_server, settings.smtp_port, timeout=60)
            server.starttls()

        server.login(settings.smtp_username, settings.smtp_password)

        # EmailMessage.as_bytes() encodes everything properly as UTF-8
        server.send_message(msg)

        server.quit()
        logger.info(f"Email sent successfully to {settings.recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
