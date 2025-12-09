import smtplib
from email.message import EmailMessage
from app.core.config import settings


def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()

    # ✅ Sender name + email
    msg["From"] = f"{settings.SMTP_SENDER_NAME} <{settings.SMTP_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        raise RuntimeError(f"Email send failed: {e}")
