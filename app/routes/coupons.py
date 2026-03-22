from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.coupon_schema import CouponCreate, CouponUpdate, CouponApply
from app.services.coupon_service import (
    create_coupon,
    get_all_coupons,
    update_coupon,
    delete_coupon,
    apply_coupon,
)
from app.utils.dependencies import require_role

router = APIRouter(prefix="/coupons", tags=["Coupons"])


# ── Apply coupon (any logged-in user) ──
@router.post("/apply")
def apply(
    data: CouponApply,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2, 3]))
):
    return apply_coupon(db, data.code, data.subtotal)


# ── Admin: list all coupons ──
@router.get("/")
def list_coupons(
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2]))
):
    coupons = get_all_coupons(db)
    return [
        {
            "id":            c.id,
            "code":          c.code,
            "discount_type": c.discount_type,
            "value":         c.value,
            "min_order":     c.min_order,
            "max_discount":  c.max_discount,
            "is_active":     c.is_active,
            "created_at":    c.created_at,
        }
        for c in coupons
    ]


# ── Admin: create coupon ──
@router.post("/")
def create(
    data: CouponCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2]))
):
    coupon = create_coupon(db, data)
    return {"message": "Coupon created", "code": coupon.code}


# ── Admin: update coupon ──
@router.put("/{coupon_id}")
def update(
    coupon_id: int,
    data: CouponUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2]))
):
    coupon = update_coupon(db, coupon_id, data)
    return {"message": "Coupon updated", "code": coupon.code}


# ── Admin: delete coupon ──
@router.delete("/{coupon_id}")
def delete(
    coupon_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2]))
):
    delete_coupon(db, coupon_id)
    return {"message": "Coupon deleted"}