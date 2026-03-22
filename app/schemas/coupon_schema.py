from pydantic import BaseModel
from typing import Optional
from app.models.coupon import DiscountType

class CouponCreate(BaseModel):
    code:          str
    discount_type: DiscountType
    value:         float = 0
    min_order:     float = 0
    max_discount:  Optional[float] = None
    is_active:     bool  = True

class CouponUpdate(BaseModel):
    value:        Optional[float] = None
    min_order:    Optional[float] = None
    max_discount: Optional[float] = None
    is_active:    Optional[bool]  = None

class CouponApply(BaseModel):
    code:     str
    subtotal: float