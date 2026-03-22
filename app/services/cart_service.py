from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.product import Product
from app.models.product_image import ProductImage

# -----------------------------
# ADD TO CART
# -----------------------------
def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    existing_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == product_id
    ).first()

    if existing_item:
        existing_item.quantity += quantity
    else:
        cart_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)

    db.commit()
    return True


# -----------------------------
# GET USER CART
# -----------------------------
def get_user_cart(db: Session, user_id: int):
    cart_items = db.query(Cart).filter(
        Cart.user_id == user_id
    ).all()

    result = []
    total_amount = 0

    for item in cart_items:
        product = item.product

        discounted_price = product.price - (
            product.price * product.discount / 100
        )
        item_total = discounted_price * item.quantity
        total_amount += item_total

        # Fetch images for this product
        images = db.query(ProductImage).filter(
            ProductImage.product_id == product.id
        ).all()

        image_urls = [f"/{img.image_url}" for img in images]

        result.append({
            "cart_id":     item.id,
            "product_id":  product.id,
            "name":        product.name,
            "category":    product.category,
            "price":       product.price,
            "discount":    product.discount,
            "final_price": round(discounted_price, 2),
            "quantity":    item.quantity,
            "item_total":  round(item_total, 2),
            "stock":       product.stock,
            "images":      image_urls,
        })

    return {
        "items": result,
        "total_amount": round(total_amount, 2)
    }


# -----------------------------
# UPDATE CART ITEM
# -----------------------------
def update_cart_item(db: Session, cart_id: int, quantity: int, user_id: int):
    cart_item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == user_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if cart_item.product.stock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    cart_item.quantity = quantity
    db.commit()
    return True


# -----------------------------
# REMOVE CART ITEM
# -----------------------------
def remove_cart_item(db: Session, cart_id: int, user_id: int):
    cart_item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == user_id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return True


# -----------------------------
# CLEAR CART
# -----------------------------
def clear_cart(db: Session, user_id: int):
    db.query(Cart).filter(
        Cart.user_id == user_id
    ).delete()

    db.commit()
    return True