from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.address_schema import AddressCreate, AddressUpdate
from app.services.address_service import (
    add_address,
    get_user_addresses,
    update_address,
    delete_address
)
from app.utils.dependencies import require_role

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/")
def create_address(
    data: AddressCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    return add_address(db, current_user.id, data)


@router.get("/")
def list_addresses(
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    return get_user_addresses(db, current_user.id)


@router.put("/{address_id}")
def modify_address(
    address_id: int,
    data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    return update_address(db, current_user.id, address_id, data)


@router.delete("/{address_id}")
def remove_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    delete_address(db, current_user.id, address_id)
    return {"message": "Address deleted successfully"}