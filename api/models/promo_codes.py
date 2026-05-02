from sqlalchemy import Column, Integer, String, Float, Boolean, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class PromoCode(Base):
    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    discount_percent = Column(Float, nullable=False)
    expiration_date = Column(DATETIME, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DATETIME, default=datetime.utcnow, nullable=False)