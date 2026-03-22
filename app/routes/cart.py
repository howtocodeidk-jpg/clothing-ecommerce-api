from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cart_schema import AddToCart, UpdateCart
from app.services.cart_service import (
    add_to_cart,
    get_user_cart,
    update_cart_item,
    remove_cart_item,
    clear_cart
)
from app.utils.dependencies import require_role
from app.core.security import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


# -----------------------------
# ADD TO CART (USER ONLY)
# -----------------------------

@router.post("/")
def add_item(
    data: AddToCart,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    add_to_cart(db, current_user.id, data.product_id, data.quantity)
    return {"message": "Product added to cart"}


# -----------------------------
# VIEW CART
# -----------------------------

@router.get("/")
def view_cart(
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    return get_user_cart(db, current_user.id)


# -----------------------------
# UPDATE CART ITEM
# -----------------------------

@router.put("/{cart_id}")
def update_item(
    cart_id: int,
    data: UpdateCart,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    update_cart_item(db, cart_id, data.quantity, current_user.id)
    return {"message": "Cart item updated successfully"}


# -----------------------------
# REMOVE CART ITEM
# -----------------------------

@router.delete("/{cart_id}")
def delete_item(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    remove_cart_item(db, cart_id, current_user.id)
    return {"message": "Item removed from cart"}


# -----------------------------
# CLEAR CART
# -----------------------------

@router.delete("/")
def clear_user_cart(
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    clear_cart(db, current_user.id)
    return {"message": "Cart cleared successfully"}