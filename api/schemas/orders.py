from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class OrderBase(BaseModel):
    order_number: str
    customer_name: str
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    order_type: str = "takeout"  # "takeout" or "delivery"
    total_price: float
    order_status: str
    order_date: datetime
    promo_code: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    order_number: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    order_type: Optional[str] = None
    total_price: Optional[float] = None
    order_status: Optional[str] = None
    order_date: Optional[datetime] = None
    promo_code: Optional[str] = None


class Order(OrderBase):
    id: int

    class ConfigDict:
        from_attributes = True
