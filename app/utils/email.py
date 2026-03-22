import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


def send_email(to_email: str, subject: str, body: str, otp: str = None):
    try:
        print(f"📧 Attempting to send email to: {to_email}")
        print(f"📧 SMTP Host: {settings.SMTP_HOST}")
        print(f"📧 SMTP Port: {settings.SMTP_PORT}")
        print(f"📧 SMTP User: {settings.SMTP_USER}")
        print(f"📧 Email From: {settings.EMAIL_FROM}")

        # Build message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = settings.EMAIL_FROM
        msg["To"]      = to_email

        # Plain text
        plain = MIMEText(body, "plain")
        msg.attach(plain)

        # HTML with styled OTP
        otp_code = otp or body
        html_body = f"""
        <html>
          <body style="margin:0;padding:0;background:#0a0a0a;
            font-family:'Helvetica Neue',sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0"
              style="background:#0a0a0a;padding:40px 20px;">
              <tr>
                <td align="center">
                  <table width="440" cellpadding="0" cellspacing="0"
                    style="background:#141414;
                    border:1px solid rgba(255,255,255,0.08);
                    border-radius:20px;padding:40px;">
                    <tr>
                      <td>
                        <h1 style="margin:0 0 6px;color:#ffffff;font-size:24px;
                          font-weight:700;">DRAPE</h1>
                        <p style="margin:0 0 28px;color:rgba(255,255,255,0.4);
                          font-size:14px;">{subject}</p>
                        <div style="background:rgba(34,197,94,0.08);
                          border:1px solid rgba(34,197,94,0.25);
                          border-radius:14px;padding:24px;
                          text-align:center;margin-bottom:24px;">
                          <p style="margin:0 0 8px;
                            color:rgba(255,255,255,0.4);font-size:12px;
                            text-transform:uppercase;letter-spacing:2px;">
                            Your verification code
                          </p>
                          <span style="font-size:42px;font-weight:800;
                            color:#22c55e;letter-spacing:10px;
                            font-family:monospace;">
                            {otp_code}
                          </span>
                        </div>
                        <p style="margin:0;color:rgba(255,255,255,0.25);
                          font-size:12px;line-height:1.6;">
                          This code expires in
                          <strong style="color:rgba(255,255,255,0.4);">
                            10 minutes
                          </strong>.<br/>
                          If you didn't request this, ignore this email.
                        </p>
                      </td>
                    </tr>
                  </table>
                  <p style="color:rgba(255,255,255,0.15);font-size:11px;
                    margin-top:20px;">
                    © 2025 DRAPE. All rights reserved.
                  </p>
                </td>
              </tr>
            </table>
          </body>
        </html>
        """
        html_part = MIMEText(html_body, "html")
        msg.attach(html_part)

        # ── Try TLS on port 587 first ──────────────────────────────
        try:
            print("📧 Trying STARTTLS on port 587...")
            server = smtplib.SMTP(settings.SMTP_HOST, 587, timeout=30)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, to_email, msg.as_string())
            server.quit()
            print(f"✅ Email sent via port 587 to: {to_email}")
            return True

        except Exception as e587:
            print(f"⚠️  Port 587 failed: {e587}")
            print("📧 Trying SSL on port 465...")

            # ── Fallback: SSL on port 465 ──────────────────────────
            context = ssl.create_default_context()
            server  = smtplib.SMTP_SSL(
                settings.SMTP_HOST, 465,
                context=context,
                timeout=30
            )
            server.ehlo()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, to_email, msg.as_string())
            server.quit()
            print(f"✅ Email sent via port 465 to: {to_email}")
            return True

    except Exception as e:
        print(f"❌ Email error: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False