from typing import Optional
from pydantic import BaseModel


class MenuItemBase(BaseModel):
    name: str
    calorie_count: Optional[int] = None
    price: float
    category: Optional[str] = None
    available: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    calorie_count: Optional[int] = None
    price: Optional[float] = None
    category: Optional[str] = None
    available: Optional[bool] = None


class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True