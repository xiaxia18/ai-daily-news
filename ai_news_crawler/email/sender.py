import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

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

    msg = MIMEMultipart("alternative")
    msg["Subject"] = Header(f"AI 每日简报 - {context['date']}", 'utf-8')
    msg["From"] = settings.smtp_username
    msg["To"] = settings.recipient_email

    # Add HTML part (must come after plain text for MIME alternative)
    # Some clients prefer the last part
    text_content = "Please view this email in an HTML-enabled email client."
    text_part = MIMEText(text_content, "plain", "utf-8")
    msg.attach(text_part)

    html_part = MIMEText(html, "html", "utf-8")
    msg.attach(html_part)

    try:
        if settings.smtp_port == 465:
            # SSL connection
            server = smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port, timeout=60)
        else:
            # STARTTLS
            server = smtplib.SMTP(settings.smtp_server, settings.smtp_port, timeout=60)
            server.starttls()

        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(msg)
        server.quit()
        logger.info(f"Email sent successfully to {settings.recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
