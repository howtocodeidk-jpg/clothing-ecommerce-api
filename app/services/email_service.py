import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


def send_email(to_email: str, subject: str, body: str):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = settings.EMAIL_FROM
        msg["To"]      = to_email

        # Plain text
        msg.attach(MIMEText(body, "plain"))

        # HTML
        html = f"""
        <html>
          <body style="margin:0;padding:0;background:#0a0a0a;font-family:sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0"
              style="background:#0a0a0a;padding:40px 20px;">
              <tr>
                <td align="center">
                  <table width="420" cellpadding="0" cellspacing="0"
                    style="background:#141414;border:1px solid rgba(255,255,255,0.08);
                    border-radius:20px;padding:40px;">
                    <tr>
                      <td>
                        <h2 style="margin:0 0 8px;color:#fff;font-size:22px;">DRAPE</h2>
                        <p style="margin:0 0 24px;color:rgba(255,255,255,0.4);font-size:14px;">
                          {subject}
                        </p>
                        <p style="margin:0 0 8px;color:rgba(255,255,255,0.3);font-size:12px;
                          text-transform:uppercase;letter-spacing:2px;">
                          {body}
                        </p>
                        <p style="margin:24px 0 0;color:rgba(255,255,255,0.2);font-size:12px;">
                          This code expires in 10 minutes. Do not share it.
                        </p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </body>
        </html>
        """
        msg.attach(MIMEText(html, "html"))

        # ── Connect with ehlo() first ──────────────────────────────
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30)
        server.ehlo()                          # ← this was missing
        server.starttls()
        server.ehlo()                          # ← call again after starttls
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.EMAIL_FROM, to_email, msg.as_string())
        server.quit()

        print(f"✅ Email sent to: {to_email}")
        return True

    except Exception as e:
        print(f"❌ Email error: {e}")
        return False