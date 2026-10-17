
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_email(subject: str, body: str) -> None:
    """Send an email using Gmail SMTP."""
    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = os.getenv("ALERT_EMAIL_TO")

    if not sender or not password or not recipient:
        raise ValueError(
            "Missing GMAIL_ADDRESS, GMAIL_APP_PASSWORD, "
            "or ALERT_EMAIL_TO in .env"
        )

    message = EmailMessage()
    message["From"] = f"Job Alert Bot <{sender}>"
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)

    print("Email sent successfully!")
