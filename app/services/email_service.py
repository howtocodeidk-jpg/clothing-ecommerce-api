import smtplib
from email.mime.text import MIMEText
from app.config import settings

def send_email(to_email: str, subject: str, body: str):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to_email

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
            print("Sending email to:", to_email)
            print("Subject:", subject)
            print("Body:", body)


        return True
    
    except Exception as e:
        print("Email error:", e)
        return False
