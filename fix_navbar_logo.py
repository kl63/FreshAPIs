#!/usr/bin/env python3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import sys
import json

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to sys.path
sys.path.insert(0, current_dir)

# Import models
from models.setting import StoreSetting
from database.database import SessionLocal, engine

def fix_navbar_logo():
    """Update the navbar logo path directly in the database."""
    db = SessionLocal()
    try:
        # Get the store settings record
        store_setting = db.query(StoreSetting).first()
        if not store_setting:
            print("No store settings found.")
            return
        
        # Get current navbar
        navbar = store_setting.navbar
        if navbar and isinstance(navbar, dict):
            # Update the logo path
            navbar["logo"] = "/logo/logo-color.svg"
            
            # Update the record
            store_setting.navbar = navbar
            db.commit()
            print("Navbar logo path updated successfully!")
        else:
            print("No navbar found or navbar is not a dictionary.")
    except Exception as e:
        db.rollback()
        print(f"Error updating navbar logo: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_navbar_logo()
