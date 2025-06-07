from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from schemas.category import Category

class ProductBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: float = Field(gt=0)
    discounted_price: float = Field(default=0, ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    availability: bool = True
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    unit: Optional[str] = "piece"

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_available: Optional[bool] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = None
    discount_percentage: int = 0
    image: List[str] = [] # Added for frontend compatibility

    class Config:
        from_attributes = True
        
    def __init__(self, **data):
        super().__init__(**data)
        # Convert image_url to image array for frontend compatibility
        if hasattr(self, 'image_url') and self.image_url:
            self.image = [self.image_url]
        else:
            self.image = []
