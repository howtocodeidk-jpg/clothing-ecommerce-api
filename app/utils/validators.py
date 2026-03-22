import re
from fastapi import HTTPException

def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(400, "Password must contain uppercase letter")
    if not re.search(r"[0-9]", password):
        raise HTTPException(400, "Password must contain number")

def validate_phone(phone: str):
    if not re.match(r"^\+?[1-9]\d{9,14}$", phone):
        raise HTTPException(400, "Invalid phone number format")
