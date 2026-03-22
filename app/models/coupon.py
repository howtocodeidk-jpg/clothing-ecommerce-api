from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class DiscountType(str, enum.Enum):
    percent = "percent"
    fixed   = "fixed"
    ship    = "ship"

class Coupon(Base):
    __tablename__ = "coupons"

    id            = Column(Integer, primary_key=True, index=True)
    code          = Column(String, unique=True, nullable=False, index=True)
    discount_type = Column(Enum(DiscountType), nullable=False)
    value         = Column(Float, default=0)
    min_order     = Column(Float, default=0)
    max_discount  = Column(Float, nullable=True)
    is_active     = Column(Boolean, default=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())