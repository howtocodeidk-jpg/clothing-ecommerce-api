from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.review_schema import ReviewCreate, ReviewUpdate
from app.services.review_service import (
    create_review,
    get_product_reviews,
    update_review,
    delete_review
)
from app.utils.dependencies import require_role


router = APIRouter(prefix="/reviews", tags=["Reviews"])


# CREATE REVIEW
@router.post("/")
def add_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role([3]))
):

    return create_review(db, current_user.id, review)


# GET PRODUCT REVIEWS
@router.get("/product/{product_id}")
def get_reviews(product_id: int, db: Session = Depends(get_db)):

    return get_product_reviews(db, product_id)


# UPDATE REVIEW
@router.put("/{review_id}")
def edit_review(
    review_id: int,
    data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role([3]))
):

    return update_review(db, review_id, current_user.id, data)


# DELETE REVIEW
@router.delete("/{review_id}")
def remove_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role([3]))
):

    return delete_review(db, review_id, current_user.id)