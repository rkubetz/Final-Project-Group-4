from sqlalchemy import Column, Integer, String, Float, ForeignKey, DATETIME, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
 
 
class Review(Base):
    __tablename__ = "reviews"
 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    rating = Column(Integer, nullable=False)          # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(DATETIME, default=datetime.utcnow, nullable=False)
 
    order = relationship("Order", back_populates="reviews")
    menu_item = relationship("MenuItem", back_populates="reviews")