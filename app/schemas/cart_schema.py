from pydantic import BaseModel, Field


class AddToCart(BaseModel):
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., gt=0, example=2)


class UpdateCart(BaseModel):
    quantity: int = Field(..., gt=0, example=3)