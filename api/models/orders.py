from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False)
    customer_name = Column(String(100), nullable=False)
    order_date = Column(DATETIME, default=datetime.utcnow)
    total_price = Column(Float, nullable=False)
    order_status = Column(String(100), nullable=False)

    order_details = relationship("OrderDetail", back_populates="order")
    payment_information = relationship("PaymentInformation", back_populates="order")