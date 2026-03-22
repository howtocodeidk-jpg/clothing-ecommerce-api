from fastapi import HTTPException
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate
from sqlalchemy.orm import Session


def create_product(db: Session, product_data: ProductCreate):
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_products(
    db: Session,
    search: str = None,
    category: str = None,
    size: str = None,
    min_price: float = None,
    max_price: float = None,
    gender: str = None,
    discount: float = None,
    color: str = None,
    fabric: str = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(Product).filter(Product.is_active == True)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if category:
        query = query.filter(Product.category == category)

    if size:
        query = query.filter(Product.sizes.ilike(f"%{size}%"))

    if gender:
        query = query.filter(Product.gender == gender)

    if color:
        query = query.filter(Product.colors.ilike(f"%{color}%"))

    if fabric:
        query = query.filter(Product.fabric == fabric)

    if min_price:
        query = query.filter(Product.price >= min_price)

    if max_price:
        query = query.filter(Product.price <= max_price)

    if discount:
        query = query.filter(Product.discount >= discount)

    total = query.count()

    products = query.offset((page - 1) * limit).limit(limit).all()

    return products, total

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()

def update_product(db: Session, product_id: int, data: ProductUpdate):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(404, "Product not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product

def delete_product(db: Session, product_id: int):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(404, "Product not found")

    product.is_active = False
    db.commit()

    return True
