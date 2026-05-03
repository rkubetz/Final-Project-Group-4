from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PromoCodeBase(BaseModel):
    code: str
    discount_percent: float
    expiration_date: datetime
    active: bool = True


class PromoCodeCreate(PromoCodeBase):
    pass


class PromoCodeUpdate(BaseModel):
    code: Optional[str] = None
    discount_percent: Optional[float] = None
    expiration_date: Optional[datetime] = None
    active: Optional[bool] = None


class PromoCode(PromoCodeBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True
        