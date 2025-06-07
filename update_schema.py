from sqlalchemy import create_engine, text
from core.config import settings as app_settings
from database.database import Base
import models.product  # Import all models to ensure they're registered with Base
import models.category
import models.user
import models.order
import models.setting
import models.language

def update_database():
    """
    Update the database schema to match the latest models.
    WARNING: This will drop and recreate all tables, causing data loss!
    """
    # Create engine
    engine = create_engine(app_settings.DATABASE_URL)
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped successfully")
    
    # Create all tables with the new schema
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully with the new schema")

if __name__ == "__main__":
    # Security prompt
    confirm = input("WARNING: This will delete all data in the database. Type 'YES' to confirm: ")
    if confirm == "YES":
        update_database()
    else:
        print("Operation cancelled.")
