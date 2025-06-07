from sqlalchemy import inspect, text
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database import engine

def update_store_settings_table():
    # Create a connection
    with engine.begin() as conn:
        # Check if columns exist before adding them
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('store_settings')]
        
        # Add navbar column if it doesn't exist
        if 'navbar' not in columns:
            conn.execute(text('ALTER TABLE store_settings ADD COLUMN navbar JSON DEFAULT NULL'))
            print("Added 'navbar' column to store_settings table")
        
        # Add footer column if it doesn't exist
        if 'footer' not in columns:
            conn.execute(text('ALTER TABLE store_settings ADD COLUMN footer JSON DEFAULT NULL'))
            print("Added 'footer' column to store_settings table")
        
        # Add logo column if it doesn't exist
        if 'logo' not in columns:
            conn.execute(text('ALTER TABLE store_settings ADD COLUMN logo VARCHAR(255) DEFAULT NULL'))
            print("Added 'logo' column to store_settings table")
    
    print("Database schema update completed successfully.")

if __name__ == "__main__":
    update_store_settings_table()
