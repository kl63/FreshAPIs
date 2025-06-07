from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, func
from sqlalchemy.sql import expression
from database.database import Base

class Coupon(Base):
    __tablename__ = "coupons"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    discount_type = Column(String, nullable=False)  # 'percentage' or 'fixed'
    discount_value = Column(Float, nullable=False)  # percentage or amount
    minimum_purchase = Column(Float, default=0)
    active = Column(Boolean, server_default=expression.true(), nullable=False)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
