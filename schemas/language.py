from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LanguageBase(BaseModel):
    name: str
    code: str
    flag: Optional[str] = None
    is_default: bool = False
    is_active: bool = True

class LanguageCreate(LanguageBase):
    pass

class LanguageUpdate(BaseModel):
    name: Optional[str] = None
    flag: Optional[str] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None

class Language(LanguageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
