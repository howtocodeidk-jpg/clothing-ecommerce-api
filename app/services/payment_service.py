import razorpay
from fastapi import HTTPException
from app.config import settings

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

def create_razorpay_order(amount: float):

    try:
        payment = client.order.create({
            "amount": int(amount * 100),   # paise
            "currency": "INR",
            "payment_capture": 1
        })

        return payment

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))