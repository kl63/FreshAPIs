from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database.database import get_db
from models.setting import StoreSetting, GlobalSetting
from schemas.setting import (
    StoreSetting as StoreSettingSchema, 
    StoreSeoSetting, 
    StoreCustomizationSetting,
    StoreSettingCreate, 
    StoreSettingUpdate, 
    GlobalSetting as GlobalSettingSchema, 
    GlobalSettingCreate, 
    GlobalSettingUpdate
)
from core.security import get_current_admin_user

router = APIRouter(
    prefix="/setting",
    tags=["Settings"],
    responses={404: {"description": "Not found"}},
)

# Initialize default store settings if not exist
async def get_or_create_store_settings(db: Session):
    db_setting = db.query(StoreSetting).first()
    if not db_setting:
        # Default navbar items
        default_navbar = {
            "logo": "/logo/logo-color.svg",
            "menu_items": [
                {"title": "Home", "href": "/"},
                {"title": "Shop", "href": "/search"},
                {"title": "About Us", "href": "/about-us"},
                {"title": "Contact Us", "href": "/contact-us"}
            ]
        }
        
        # Default footer items
        default_footer = {
            "copyright_text": "© 2025 Freshly Supermarket. All rights reserved.",
            "social_links": {
                "facebook": "https://facebook.com",
                "twitter": "https://twitter.com",
                "instagram": "https://instagram.com"
            },
            "company_info": [
                {"title": "About Us", "href": "/about-us"},
                {"title": "Contact Us", "href": "/contact-us"},
                {"title": "Terms & Conditions", "href": "/terms"},
                {"title": "Privacy Policy", "href": "/privacy-policy"}
            ],
            "customer_care": [
                {"title": "FAQ", "href": "/faq"},
                {"title": "Returns", "href": "/returns"},
                {"title": "Shipping", "href": "/shipping"}
            ]
        }
        
        # Create default store settings
        db_setting = StoreSetting(
            store_name="Freshly Supermarket",
            store_email="info@freshlysupermarket.com",
            meta_title="Freshly Supermarket - Your Go-to Grocery Store",
            meta_description="Shop fresh groceries, household essentials and more at Freshly Supermarket. Quick delivery, great prices!",
            navbar=default_navbar,
            footer=default_footer,
            logo="/logo/logo-color.svg"
        )
        db.add(db_setting)
        db.commit()
        db.refresh(db_setting)
    
    # If existing settings have no navbar/footer, add defaults
    if not db_setting.navbar:
        db_setting.navbar = {
            "logo": "/logo/logo-color.svg",
            "menu_items": [
                {"title": "Home", "href": "/"},
                {"title": "Shop", "href": "/search"},
                {"title": "About Us", "href": "/about-us"},
                {"title": "Contact Us", "href": "/contact-us"}
            ]
        }
        db.commit()
    
    # Update existing logo paths if they're pointing to non-existent files
    if db_setting.logo == "/logo.svg":
        db_setting.logo = "/logo/logo-color.svg"
        db.commit()
        
    # Update existing navbar logo if it's pointing to non-existent files
    if db_setting.navbar and isinstance(db_setting.navbar, dict) and db_setting.navbar.get("logo") == "/logo.svg":
        db_setting.navbar["logo"] = "/logo/logo-color.svg"
        db.commit()
    
    return db_setting

# Initialize default global settings if not exist
async def get_or_create_global_settings(db: Session):
    db_setting = db.query(GlobalSetting).first()
    if not db_setting:
        # Create default global settings
        db_setting = GlobalSetting()
        db.add(db_setting)
        db.commit()
        db.refresh(db_setting)
    return db_setting

@router.get("/store-setting/all", response_model=StoreSettingSchema)
async def get_store_settings(db: Session = Depends(get_db)):
    """Get all store settings"""
    db_setting = await get_or_create_store_settings(db)
    return db_setting

@router.get("/store-setting/seo", response_model=StoreSeoSetting)
async def get_store_seo_settings(db: Session = Depends(get_db)):
    """Get SEO settings for the store"""
    db_setting = await get_or_create_store_settings(db)
    return db_setting

@router.get("/store/customization/all", response_model=StoreCustomizationSetting)
async def get_store_customization_settings(db: Session = Depends(get_db)):
    """Get customization settings for the store"""
    db_setting = await get_or_create_store_settings(db)
    return db_setting

@router.put("/store-setting", response_model=StoreSettingSchema)
async def update_store_settings(
    setting: StoreSettingUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """Update store settings - admin only"""
    db_setting = await get_or_create_store_settings(db)
    
    # Update fields
    update_data = setting.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_setting, key, value)
    
    db.commit()
    db.refresh(db_setting)
    return db_setting

@router.get("/global/all", response_model=GlobalSettingSchema)
async def get_global_settings(db: Session = Depends(get_db)):
    """Get global settings"""
    db_setting = await get_or_create_global_settings(db)
    return db_setting

@router.put("/global", response_model=GlobalSettingSchema)
async def update_global_settings(
    setting: GlobalSettingUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """Update global settings - admin only"""
    db_setting = await get_or_create_global_settings(db)
    
    # Update fields
    update_data = setting.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_setting, key, value)
    
    db.commit()
    db.refresh(db_setting)
    return db_setting
