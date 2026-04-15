from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class PaymentInformation(Base):
    __tablename__ = "payment_information"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_type = Column(String(50), nullable=False)
    card_brand = Column(String(50), nullable=True)
    transaction_status = Column(String(50), nullable=False)
    created_at = Column(DATETIME, default=datetime.utcnow, nullable=False)

    order = relationship("Order", back_populates="payment_information")