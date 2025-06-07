from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None

class SubCategory(BaseModel):
    id: int
    name: str
    slug: str
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    children: List[SubCategory] = []

    class Config:
        from_attributes = True
