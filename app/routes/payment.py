from fastapi import APIRouter
from app.schemas.payment_schema import CreatePayment, VerifyPayment
from app.services.payment_service import create_razorpay_order
from app.config import settings
import razorpay

router = APIRouter(prefix="/payments", tags=["Payments"])

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


@router.post("/create")
def create_payment(data: CreatePayment):

    order = create_razorpay_order(data.amount)

    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "key": settings.RAZORPAY_KEY_ID
    }


@router.post("/verify")
def verify_payment(data: VerifyPayment):

    params = {
        "razorpay_order_id": data.razorpay_order_id,
        "razorpay_payment_id": data.razorpay_payment_id,
        "razorpay_signature": data.razorpay_signature
    }

    try:
        client.utility.verify_payment_signature(params)

        return {
            "message": "Payment verified successfully"
        }

    except:
        raise Exception("Payment verification failed")