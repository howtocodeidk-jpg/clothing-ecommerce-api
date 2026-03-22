from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    phone = Column(String)
    code = Column(String)
    expires_at = Column(DateTime)
    attempts = Column(Integer, default=0)
