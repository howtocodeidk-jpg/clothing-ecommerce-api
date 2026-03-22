from pydantic import BaseModel
from typing import Optional, List

class ProductCreate(BaseModel):
    name: str
    category: str
    gender: str
    description: str
    price: float
    discount: float = 0
    sizes: List[str]
    colors: List[str]
    fabric: str
    stock: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    gender: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    discount: Optional[float] = None
    sizes: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    fabric: Optional[str] = None
    stock: Optional[int] = None
