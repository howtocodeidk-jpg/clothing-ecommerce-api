import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY   = os.getenv("SECRET_KEY")

    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS   = 7
    OTP_EXPIRE_MINUTES          = 5

    # Gmail SMTP — free forever
    EMAIL_FROM    = os.getenv("EMAIL_FROM",    "")
    SMTP_HOST     = os.getenv("SMTP_HOST",     "smtp.gmail.com")
    SMTP_PORT     = int(os.getenv("SMTP_PORT", 465))
    SMTP_USER     = os.getenv("SMTP_USER",     "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").replace(" ", "")

    # Razorpay
    RAZORPAY_KEY_ID     = os.getenv("RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")


settings = Settings()