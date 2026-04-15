from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    calorie_count = Column(Integer, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=True)
    available = Column(Boolean, default=True, nullable=False)

    order_details = relationship("OrderDetail", back_populates="menu_item")
    recipes = relationship("Recipe", back_populates="menu_item")