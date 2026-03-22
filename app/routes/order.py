from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.order_schema import PlaceOrder, OrderStatusUpdate
from app.services.order_service import (
    cancel_order,
    create_order,
    get_user_orders,
    get_all_orders,
    update_order_status
)
from app.utils.dependencies import require_role

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def place_order(
    data: PlaceOrder,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    order = create_order(db, current_user.id, data.address_id)

    return {
        "message": "Order placed successfully",
        "order_id": order.id,
        "total_amount": order.total_amount,
        "status": order.status
    }

@router.get("/")
def my_orders(
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    return get_user_orders(db, current_user.id)

@router.get("/all")
def all_orders(
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2]))
):
    return get_all_orders(db)

@router.put("/{order_id}/status")
def change_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2]))
):
    order = update_order_status(db, order_id, data.status)

    return {
        "message": "Order status updated successfully",
        "order_id": order.id,
        "new_status": order.status
    }

@router.put("/{order_id}/cancel")
def cancel_user_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([3]))
):
    order = cancel_order(db, order_id, current_user.id)

    return {
        "message": "Order cancelled successfully",
        "order_id": order.id,
        "status": order.status
    } 