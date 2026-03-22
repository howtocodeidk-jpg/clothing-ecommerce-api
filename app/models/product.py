from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    gender = Column(String, nullable=False)  
    description = Column(Text, nullable=False)

    price = Column(Float, nullable=False)
    discount = Column(Float, default=0)

    sizes = Column(String)      
    colors = Column(String)     
    fabric = Column(String)
    stock = Column(Integer, default=0)
    images = relationship("ProductImage", back_populates="product")

    is_active = Column(Boolean, default=True)

    cart_items = relationship("Cart", back_populates="product", cascade="all, delete")
