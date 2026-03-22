from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
import uuid

from app.database import get_db
from app.models.product import Product
from app.models.product_image import ProductImage
from app.services.product_service import *
from app.utils.dependencies import require_role

router = APIRouter(prefix="/products", tags=["Products"])


# --------------------------------------------------
# GET - PRODUCT LISTING (ALL ROLES)
# --------------------------------------------------

@router.get("/")
def list_products(
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
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2, 3]))
):
    products, total = get_products(
        db, search, category, size,
        min_price, max_price, gender,
        discount, color, fabric,
        page, limit
    )

    response_data = []

    for product in products:
        response_data.append({
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "description": product.description,
            "gender": product.gender,
            "price": product.price,
            "discount": product.discount,
            "stock": product.stock,
            "images": [
                f"/{img.image_url}" for img in product.images
            ]
        })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": response_data
    }


# --------------------------------------------------
# GET - PRODUCT DETAILS
# --------------------------------------------------

@router.get("/{product_id}")
def product_details(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2, 3]))
):
    product = get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "gender": product.gender,
        "description": product.description,
        "price": product.price,
        "discount": product.discount,
        "sizes": product.sizes,
        "colors": product.colors,
        "fabric": product.fabric,
        "stock": product.stock,
        "images": [
            f"/{img.image_url}" for img in product.images
        ]
    }


# --------------------------------------------------
# CREATE PRODUCT (ADMIN & SUPERADMIN)
# --------------------------------------------------

@router.post("/")
def create_new_product(
    name: str = Form(...),
    category: str = Form(...),
    gender: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    discount: float = Form(0),
    sizes: str = Form(...),
    colors: str = Form(...),
    fabric: str = Form(...),
    stock: int = Form(...),
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2]))
):

    product = Product(
        name=name,
        category=category,
        gender=gender,
        description=description,
        price=price,
        discount=discount,
        sizes=sizes,
        colors=colors,
        fabric=fabric,
        stock=stock
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    # Ensure upload directory exists
    os.makedirs("uploads/products", exist_ok=True)

    for image in images:
        file_extension = image.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = f"uploads/products/{filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        product_image = ProductImage(
            image_url=file_path,
            product_id=product.id
        )

        db.add(product_image)

    db.commit()

    return {"message": "Product created successfully"}


# --------------------------------------------------
# UPDATE PRODUCT (ADMIN & SUPERADMIN)
# --------------------------------------------------

@router.put("/{product_id}")
def update_existing_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2]))
):
    product = update_product(db, product_id, product_data)

    return {
        "message": "Product updated successfully",
        "data": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        }
    }


# --------------------------------------------------
# DELETE PRODUCT (SOFT DELETE)
# --------------------------------------------------

@router.delete("/{product_id}")
def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2]))
):
    delete_product(db, product_id)

    return {"message": "Product deleted successfully"}
