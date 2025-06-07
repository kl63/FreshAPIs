from sqlalchemy import text
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database import engine, SessionLocal
from models.setting import StoreSetting

def update_store_settings_footer():
    """Update existing store settings to include footer and logo data"""
    db = SessionLocal()
    try:
        # Get existing record
        store_setting = db.query(StoreSetting).first()
        if store_setting:
            # Default footer data
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
            
            # Update footer if it's null
            if not store_setting.footer:
                store_setting.footer = default_footer
                print("Updated footer data")
            
            # Update logo if it's null
            if not store_setting.logo:
                store_setting.logo = "/logo.svg"
                print("Updated logo")
            
            db.commit()
            print("Successfully updated store settings")
        else:
            print("No store settings found")
    finally:
        db.close()

if __name__ == "__main__":
    update_store_settings_footer()
