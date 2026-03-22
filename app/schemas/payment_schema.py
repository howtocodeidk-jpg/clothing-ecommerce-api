from pydantic import BaseModel

class CreatePayment(BaseModel):
    amount: float


class VerifyPayment(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str