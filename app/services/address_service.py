from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.address import Address


# -----------------------------
# ADD ADDRESS
# -----------------------------

def add_address(db: Session, user_id: int, data):

    if data.is_default:
        db.query(Address).filter(
            Address.user_id == user_id
        ).update({"is_default": False})

    address = Address(
        user_id=user_id,
        full_name=data.full_name,
        phone=data.phone,
        address_line=data.address_line,
        city=data.city,
        state=data.state,
        postal_code=data.postal_code,
        country=data.country,
        is_default=data.is_default
    )

    db.add(address)
    db.commit()
    db.refresh(address)

    return address


# -----------------------------
# GET USER ADDRESSES
# -----------------------------

def get_user_addresses(db: Session, user_id: int):
    return db.query(Address).filter(
        Address.user_id == user_id
    ).all()


# -----------------------------
# UPDATE ADDRESS
# -----------------------------

def update_address(db: Session, user_id: int, address_id: int, data):

    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    if data.is_default:
        db.query(Address).filter(
            Address.user_id == user_id
        ).update({"is_default": False})

    for key, value in data.dict(exclude_unset=True).items():
        setattr(address, key, value)

    db.commit()
    return address


# -----------------------------
# DELETE ADDRESS
# -----------------------------

def delete_address(db: Session, user_id: int, address_id: int):

    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(address)
    db.commit()

    return True