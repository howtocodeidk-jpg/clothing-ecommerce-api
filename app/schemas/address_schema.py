from pydantic import BaseModel, Field
from typing import Optional


class AddressCreate(BaseModel):
    full_name: str = Field(..., example="John Doe")
    phone: str = Field(..., example="9876543210")
    address_line: str = Field(..., example="123 Main Street")
    city: str = Field(..., example="New York")
    state: str = Field(..., example="NY")
    postal_code: str = Field(..., example="10001")
    country: str = Field(..., example="USA")
    is_default: Optional[bool] = False


class AddressUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address_line: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = None