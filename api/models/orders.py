from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=True)
    customer_address = Column(String(255), nullable=True)
    order_type = Column(String(20), nullable=False, default="takeout") # "takeout" or "delivery"
    order_date = Column(DATETIME, default=datetime.utcnow)
    total_price = Column(Float, nullable=False)
    order_status = Column(String(100), nullable=False)
    promo_code = Column(String(50), nullable=True)

    order_details = relationship("OrderDetail", back_populates="order")
    payment_information = relationship("PaymentInformation", back_populates="order")
    reviews = relationship("Review", back_populates="order")