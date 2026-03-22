import resend
from app.config import settings


def send_email(to_email: str, subject: str, body: str):
    try:
        resend.api_key = settings.RESEND_API_KEY

        html = f"""
        <html>
          <body style="margin:0;padding:0;background:#0a0a0a;font-family:sans-serif;">
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
                            font-size:11px;text-transform:uppercase;
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
                          If you didn't request this, you can safely
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

        response = resend.Emails.send({
            "from":    "DRAPE <onboarding@resend.dev>",
            "to":      [to_email],
            "subject": subject,
            "html":    html,
            "text":    body,
        })

        print(f"✅ Email sent to: {to_email} | ID: {response['id']}")
        return True

    except Exception as e:
        print(f"❌ Email error: {e}")
        return False