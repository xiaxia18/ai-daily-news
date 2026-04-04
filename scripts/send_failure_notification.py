#!/usr/bin/env python3
"""Send failure notification email when GitHub Actions fails."""

import os
import smtplib
from email.mime.text import MIMEText


def main():
    smtp_server = os.environ['SMTP_SERVER']
    smtp_port = int(os.environ['SMTP_PORT'])
    username = os.environ['SMTP_USERNAME']
    password = os.environ['SMTP_PASSWORD']
    recipient = os.environ['RECIPIENT_EMAIL']

    msg = MIMEText('The daily AI news crawler failed. Please check the GitHub Actions run.')
    msg['Subject'] = 'ALERT: AI Daily Briefing Failed'
    msg['From'] = username
    msg['To'] = recipient

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

    print("Failure notification sent successfully")


if __name__ == "__main__":
    main()
