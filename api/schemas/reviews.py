from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    order_id: int
    menu_item_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class Review(ReviewBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True
        