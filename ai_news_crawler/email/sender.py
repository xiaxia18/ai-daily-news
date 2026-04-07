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

    # CRITICAL: Replace ALL non-breaking spaces (\xa0) with regular spaces
    # This MUST happen before creating the email message to prevent ASCII encoding errors
    html = html.replace('\xa0', ' ')
    html = html.replace(u'\xa0', ' ')

    # Clean date string as well
    date_str = context['date'].replace('\xa0', ' ').replace(u'\xa0', ' ')

    # Use EmailMessage API which properly handles UTF-8 in Python 3
    msg = EmailMessage()
    # EmailMessage automatically encodes header values properly when containing non-ASCII chars
    msg['Subject'] = f"AI 每日简报 - {date_str}"
    msg['From'] = settings.smtp_username
    msg['To'] = settings.recipient_email

    # Set content with explicit UTF-8 charset
    # This tells SMTP to use 8-bit transfer encoding automatically
    msg.set_content(html, subtype='html', charset='utf-8')

    try:
        if settings.smtp_port == 465:
            server = smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port, timeout=60)
        else:
            server = smtplib.SMTP(settings.smtp_server, settings.smtp_port, timeout=60)
            server.starttls()

        server.login(settings.smtp_username.replace('\xa0', '').replace(u'\xa0', ''), settings.smtp_password.replace('\xa0', '').replace(u'\xa0', ''))

        # Get message as bytes for debugging
        msg_bytes = msg.as_bytes()
        logger.info(f"Message encoded successfully, size: {len(msg_bytes)} bytes")

        # Use send_message which properly handles bytes in Python 3
        server.send_message(msg)

        server.quit()
        logger.info(f"Email sent successfully to {settings.recipient_email}")
        return True
    except Exception as e:
        import traceback
        logger.error(f"Failed to send email: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False
