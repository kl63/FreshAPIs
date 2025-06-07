from sqlalchemy import Column, Integer, String, JSON, Boolean, Text
from sqlalchemy.orm import relationship

from database.database import Base
from models.base import TimestampMixin

class StoreSetting(Base, TimestampMixin):
    __tablename__ = "store_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String(100), nullable=False)
    store_email = Column(String(100), nullable=False)
    store_phone = Column(String(20), nullable=True)
    store_address = Column(Text, nullable=True)
    store_currency = Column(String(10), default="USD")
    
    # SEO fields
    meta_title = Column(String(100), nullable=True)
    meta_description = Column(Text, nullable=True)
    meta_keywords = Column(String(255), nullable=True)
    og_image = Column(String(255), nullable=True)
    favicon = Column(String(255), nullable=True)
    
    # Customization fields
    primary_color = Column(String(20), default="#10B981")
    secondary_color = Column(String(20), default="#3B82F6")
    allow_guest_checkout = Column(Boolean, default=True)
    
    # UI Customization
    navbar = Column(JSON, default=dict)
    footer = Column(JSON, default=dict)
    logo = Column(String(255), nullable=True)

class GlobalSetting(Base, TimestampMixin):
    __tablename__ = "global_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    maintenance_mode = Column(Boolean, default=False)
    language = Column(String(10), default="en")
    default_timezone = Column(String(50), default="UTC")
