from pydantic import BaseModel
from typing import Optional


class ReviewCreate(BaseModel):

    product_id: int
    rating: int
    comment: Optional[str] = None


class ReviewUpdate(BaseModel):

    rating: Optional[int] = None
    comment: Optional[str] = None


class ReviewResponse(BaseModel):

    id: int
    product_id: int
    user_id: int
    rating: int
    comment: Optional[str]

    class Config:
        from_attributes = True