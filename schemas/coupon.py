from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CouponBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_type: str  # 'percentage' or 'fixed'
    discount_value: float
    minimum_purchase: float = 0.0
    active: bool = True
    start_date: datetime = None
    end_date: Optional[datetime] = None

class CouponCreate(CouponBase):
    pass

class CouponUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    discount_type: Optional[str] = None  # 'percentage' or 'fixed'
    discount_value: Optional[float] = None
    minimum_purchase: Optional[float] = None
    active: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class Coupon(CouponBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
