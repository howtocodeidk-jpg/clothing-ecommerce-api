import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


def send_email(to_email: str, subject: str, body: str):
    try:
        print(f"📧 Sending email to: {to_email}")
        print(f"📧 Using: {settings.SMTP_USER} via {settings.SMTP_HOST}:465")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = settings.EMAIL_FROM
        msg["To"]      = to_email

        # Plain text
        msg.attach(MIMEText(body, "plain"))

        # HTML
        html = f"""
        <html>
          <body style="margin:0;padding:0;background:#0a0a0a;
            font-family:sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0"
              style="background:#0a0a0a;padding:40px 20px;">
              <tr>
                <td align="center">
                  <table width="420" cellpadding="0" cellspacing="0"
                    style="background:#141414;
                    border:1px solid rgba(255,255,255,0.08);
                    border-radius:20px;padding:40px;">
                    <tr>
                      <td>
                        <h2 style="margin:0 0 8px;color:#ffffff;
                          font-size:24px;font-weight:700;">
                          DRAPE
                        </h2>
                        <p style="margin:0 0 28px;
                          color:rgba(255,255,255,0.4);
                          font-size:14px;">
                          {subject}
                        </p>
                        <div style="background:rgba(34,197,94,0.08);
                          border:1px solid rgba(34,197,94,0.25);
                          border-radius:14px;padding:28px;
                          text-align:center;margin-bottom:24px;">
                          <p style="margin:0 0 10px;
                            color:rgba(255,255,255,0.35);
                            font-size:11px;
                            text-transform:uppercase;
                            letter-spacing:3px;">
                            Verification Code
                          </p>
                          <p style="margin:0;font-size:15px;
                            color:rgba(255,255,255,0.7);
                            line-height:1.7;font-weight:500;">
                            {body}
                          </p>
                        </div>
                        <p style="margin:0;
                          color:rgba(255,255,255,0.2);
                          font-size:12px;line-height:1.6;">
                          If you didn't request this,
                          ignore this email.
                        </p>
                      </td>
                    </tr>
                  </table>
                  <p style="color:rgba(255,255,255,0.15);
                    font-size:11px;margin-top:20px;">
                    © 2025 DRAPE. All rights reserved.
                  </p>
                </td>
              </tr>
            </table>
          </body>
        </html>
        """
        msg.attach(MIMEText(html, "html"))

        # Use SSL on port 465 — works on Render free plan
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            settings.SMTP_HOST,
            465,
            context=context,
            timeout=30
        ) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(
                settings.EMAIL_FROM,
                to_email,
                msg.as_string()
            )

        print(f"✅ Email sent to: {to_email}")
        return True

    except Exception as e:
        print(f"❌ Email error: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False