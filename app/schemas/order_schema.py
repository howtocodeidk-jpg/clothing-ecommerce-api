from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class PlaceOrder(BaseModel):
    address_id: int = Field(..., example=1)


class OrderStatusUpdate(BaseModel):
    status: str = Field(..., example="Shipped")


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        orm_mode = True


class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True