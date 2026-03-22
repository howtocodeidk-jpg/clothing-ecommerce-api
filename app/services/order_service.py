from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.address import Address


# -----------------------------
# CREATE ORDER
# -----------------------------

def create_order(db: Session, user_id: int, address_id: int):

    # Validate Address
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()

    if not address:
        raise HTTPException(status_code=400, detail="Invalid address")

    # Get Cart Items
    cart_items = db.query(Cart).filter(
        Cart.user_id == user_id
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0

    # Check stock & calculate total
    for item in cart_items:

        if item.product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {item.product.name}"
            )

        discounted_price = item.product.price - (
            item.product.price * item.product.discount / 100
        )

        total_amount += discounted_price * item.quantity

    # Create Order
    order = Order(
        user_id=user_id,
        address_id=address_id,
        total_amount=total_amount,
        status="Pending"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    # Create Order Items & Reduce Stock
    for item in cart_items:

        discounted_price = item.product.price - (
            item.product.price * item.product.discount / 100
        )

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price=discounted_price
        )

        item.product.stock -= item.quantity

        db.add(order_item)

    # Clear Cart
    db.query(Cart).filter(Cart.user_id == user_id).delete()

    db.commit()

    return order


# -----------------------------
# GET USER ORDERS
# -----------------------------

def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(
        Order.user_id == user_id
    ).all()


# -----------------------------
# GET ALL ORDERS (ADMIN)
# -----------------------------

def get_all_orders(db: Session):
    return db.query(Order).all()


# -----------------------------
# UPDATE ORDER STATUS (ADMIN)
# -----------------------------

def update_order_status(db: Session, order_id: int, status: str):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()

    return order

# -----------------------------
# CANCEL ORDER (USER)
# -----------------------------

def cancel_order(db: Session, order_id: int, user_id: int):

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status in ["Shipped", "Delivered"]:
        raise HTTPException(
            status_code=400,
            detail="Order cannot be cancelled at this stage"
        )

    if order.status == "Cancelled":
        raise HTTPException(
            status_code=400,
            detail="Order already cancelled"
        )

    # Restore stock
    for item in order.items:
        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        product.stock += item.quantity

    order.status = "Cancelled"
    db.commit()

    return order