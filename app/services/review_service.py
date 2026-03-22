from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.review import Review
from app.models.product import Product


def create_review(db: Session, user_id: int, data):

    product = db.query(Product).filter(
        Product.id == data.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    review = Review(
        user_id=user_id,
        product_id=data.product_id,
        rating=data.rating,
        comment=data.comment
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


def get_product_reviews(db: Session, product_id: int):

    reviews = db.query(Review).filter(
        Review.product_id == product_id
    ).all()

    return reviews


def update_review(db: Session, review_id: int, user_id: int, data):

    review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == user_id
    ).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if data.rating is not None:
        review.rating = data.rating

    if data.comment is not None:
        review.comment = data.comment

    db.commit()
    db.refresh(review)

    return review


def delete_review(db: Session, review_id: int, user_id: int):

    review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == user_id
    ).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()

    return {"message": "Review deleted"}