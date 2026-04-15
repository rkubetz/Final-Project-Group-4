from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PaymentInformationBase(BaseModel):
    order_id: int
    payment_type: str
    card_brand: Optional[str] = None
    transaction_status: str


class PaymentInformationCreate(PaymentInformationBase):
    pass


class PaymentInformationUpdate(BaseModel):
    order_id: Optional[int] = None
    payment_type: Optional[str] = None
    card_brand: Optional[str] = None
    transaction_status: Optional[str] = None


class PaymentInformation(PaymentInformationBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True