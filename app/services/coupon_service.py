from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.coupon import Coupon

def create_coupon(db: Session, data):
    existing = db.query(Coupon).filter(
        Coupon.code == data.code.upper().strip()
    ).first()
    if existing:
        raise HTTPException(400, "Coupon code already exists")

    coupon = Coupon(
        code          = data.code.upper().strip(),
        discount_type = data.discount_type,
        value         = data.value,
        min_order     = data.min_order,
        max_discount  = data.max_discount,
        is_active     = data.is_active,
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

def get_all_coupons(db: Session):
    return db.query(Coupon).order_by(Coupon.created_at.desc()).all()

def update_coupon(db: Session, coupon_id: int, data):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(404, "Coupon not found")
    if data.value        is not None: coupon.value        = data.value
    if data.min_order    is not None: coupon.min_order    = data.min_order
    if data.max_discount is not None: coupon.max_discount = data.max_discount
    if data.is_active    is not None: coupon.is_active    = data.is_active
    db.commit()
    db.refresh(coupon)
    return coupon

def delete_coupon(db: Session, coupon_id: int):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(404, "Coupon not found")
    db.delete(coupon)
    db.commit()
    return True

def apply_coupon(db: Session, code: str, subtotal: float):
    coupon = db.query(Coupon).filter(
        Coupon.code      == code.upper().strip(),
        Coupon.is_active == True
    ).first()

    if not coupon:
        raise HTTPException(400, "Invalid or expired coupon code")

    if subtotal < coupon.min_order:
        raise HTTPException(
            400,
            f"Minimum order of ₹{coupon.min_order:.0f} required for this coupon"
        )

    discount  = 0.0
    free_ship = False

    if coupon.discount_type == "percent":
        discount = round(subtotal * coupon.value / 100, 2)
        if coupon.max_discount:
            discount = min(discount, coupon.max_discount)

    elif coupon.discount_type == "fixed":
        discount = min(coupon.value, subtotal)

    elif coupon.discount_type == "ship":
        free_ship = True

    return {
        "valid":      True,
        "code":       coupon.code,
        "label":      _label(coupon),
        "discount":   discount,
        "free_ship":  free_ship,
        "type":       coupon.discount_type,
        "value":      coupon.value,
    }

def _label(coupon):
    if coupon.discount_type == "percent": return f"{coupon.value:.0f}% off"
    if coupon.discount_type == "fixed":   return f"₹{coupon.value:.0f} off"
    if coupon.discount_type == "ship":    return "Free shipping"
    return ""