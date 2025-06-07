from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AttributeValueBase(BaseModel):
    name: str
    value: str
    is_active: bool = True

class AttributeValueCreate(AttributeValueBase):
    pass

class AttributeValueUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    is_active: Optional[bool] = None

class AttributeValue(AttributeValueBase):
    id: int
    attribute_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AttributeBase(BaseModel):
    name: str
    slug: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True

class AttributeCreate(AttributeBase):
    values: List[AttributeValueCreate] = []

class AttributeUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class Attribute(AttributeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    values: List[AttributeValue] = []

    class Config:
        from_attributes = True
