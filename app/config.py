import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL")

    SECRET_KEY = os.getenv("SECRET_KEY")

    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS   = 7
    OTP_EXPIRE_MINUTES          = 5

    # Email via Resend (SMTP is blocked on Render free plan)
    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

    # Razorpay
    RAZORPAY_KEY_ID     = os.getenv("RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")


settings = Settings()
