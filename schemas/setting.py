from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime

class StoreSettingBase(BaseModel):
    store_name: str
    store_email: EmailStr
    store_phone: Optional[str] = None
    store_address: Optional[str] = None
    store_currency: str = "USD"
    
    # SEO fields
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    og_image: Optional[str] = None
    favicon: Optional[str] = None
    
    # Customization fields
    primary_color: str = "#10B981"
    secondary_color: str = "#3B82F6"
    allow_guest_checkout: bool = True

class StoreSettingCreate(StoreSettingBase):
    pass

class StoreSettingUpdate(BaseModel):
    store_name: Optional[str] = None
    store_email: Optional[EmailStr] = None
    store_phone: Optional[str] = None
    store_address: Optional[str] = None
    store_currency: Optional[str] = None
    
    # SEO fields
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    og_image: Optional[str] = None
    favicon: Optional[str] = None
    
    # Customization fields
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    allow_guest_checkout: Optional[bool] = None

class StoreSetting(StoreSettingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StoreSeoSetting(BaseModel):
    store_name: str
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    og_image: Optional[str] = None
    favicon: Optional[str] = None
    
    class Config:
        from_attributes = True

class NavItem(BaseModel):
    title: str
    href: str

class NavbarConfig(BaseModel):
    logo: Optional[str] = None
    menu_items: List[NavItem] = []

class FooterConfig(BaseModel):
    copyright_text: Optional[str] = None
    social_links: Dict[str, str] = {}
    company_info: List[NavItem] = []
    customer_care: List[NavItem] = []

class StoreCustomizationSetting(BaseModel):
    primary_color: str
    secondary_color: str
    allow_guest_checkout: bool
    navbar: Optional[Dict[str, Any]] = None
    footer: Optional[Dict[str, Any]] = None
    logo: Optional[str] = None
    
    class Config:
        from_attributes = True

class GlobalSettingBase(BaseModel):
    maintenance_mode: bool = False
    language: str = "en"
    default_timezone: str = "UTC"

class GlobalSettingCreate(GlobalSettingBase):
    pass

class GlobalSettingUpdate(BaseModel):
    maintenance_mode: Optional[bool] = None
    language: Optional[str] = None
    default_timezone: Optional[str] = None

class GlobalSetting(GlobalSettingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
