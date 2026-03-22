from fastapi import HTTPException
from datetime import datetime, timedelta

otp_requests = {}

def check_rate_limit(identifier: str):
    now = datetime.utcnow()
    if identifier in otp_requests:
        last_request = otp_requests[identifier]
        if now - last_request < timedelta(seconds=60):
            raise HTTPException(429, "OTP requested too frequently. Try again later.")
    otp_requests[identifier] = now
