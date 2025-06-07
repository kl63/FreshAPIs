#!/usr/bin/env python3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json
import os
import sys

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to sys.path
sys.path.insert(0, current_dir)

# Import database configuration
from database.database import SessionLocal, engine

def update_store_settings_logo():
    """Update the logo path in store settings to point to an existing logo file."""
    db = SessionLocal()
    try:
        # First, get the current settings
        result = db.execute(text("SELECT * FROM store_settings LIMIT 1")).fetchone()
        if not result:
            print("No store settings found.")
            return
            
        # Update the navbar and logo paths to use existing logo files
        updated_navbar = None
        if result.navbar:
            navbar_data = result.navbar
            # If navbar is stored as JSON string, parse it first
            if isinstance(navbar_data, str):
                navbar_data = json.loads(navbar_data)
            
            # Update the logo path in navbar
            navbar_data["logo"] = "/logo/logo-color.svg"
            updated_navbar = json.dumps(navbar_data)
        
        # Update main logo path
        # Execute SQL to update the logo path
        db.execute(
            text("UPDATE store_settings SET logo = :logo_path, navbar = :navbar_data"),
            {"logo_path": "/logo/logo-color.svg", "navbar_data": updated_navbar}
        )
        
        db.commit()
        print("Logo path updated successfully in store settings.")
    except Exception as e:
        db.rollback()
        print(f"Error updating logo path: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_store_settings_logo()
