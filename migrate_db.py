from sqlalchemy import create_engine, text
from core.config import settings as app_settings
from database.database import Base
import models.product  # Import all models to ensure they're registered with Base
import models.category
import models.user
import models.order
import models.setting
import models.language
import models.attribute

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
    
    # Create some initial data
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create a default category
    from models.category import Category
    fruits = Category(
        name="Fruits", 
        slug="fruits", 
        description="Fresh fruits from local farmers"
    )
    vegetables = Category(
        name="Vegetables", 
        slug="vegetables", 
        description="Fresh vegetables for your daily needs"
    )
    session.add(fruits)
    session.add(vegetables)
    
    # Create some sample products
    from models.product import Product
    apple = Product(
        name="Apple",
        slug="apple",
        description="Fresh red apples from local farms",
        short_description="Fresh red apples",
        price=1.99,
        discounted_price=1.49,
        stock_quantity=100,
        availability=True,
        category_id=1,  # Fruits
        image_url="/images/products/apple.jpg",
        unit="kg"
    )
    banana = Product(
        name="Banana",
        slug="banana",
        description="Yellow bananas - perfect for breakfast",
        short_description="Yellow bananas",
        price=0.99,
        stock_quantity=150,
        availability=True,
        category_id=1,  # Fruits
        image_url="/images/products/banana.jpg",
        unit="bunch"
    )
    carrot = Product(
        name="Carrot",
        slug="carrot",
        description="Orange carrots - rich in vitamin A",
        short_description="Orange carrots",
        price=1.29,
        stock_quantity=80,
        availability=True,
        category_id=2,  # Vegetables
        image_url="/images/products/carrot.jpg",
        unit="kg"
    )
    session.add(apple)
    session.add(banana)
    session.add(carrot)
    
    # Create store settings
    from models.setting import StoreSetting
    store_setting = StoreSetting(
        store_name="Freshly Supermarket",
        store_email="info@freshlysupermarket.com",
        meta_title="Freshly Supermarket - Fresh Grocery Store",
        meta_description="Shop fresh groceries, fruits, and vegetables with fast delivery",
        meta_keywords="grocery, fresh, fruits, vegetables, delivery",
        og_image="/images/logo.png",
        favicon="/favicon.ico",
        primary_color="#10B981",
        secondary_color="#3B82F6"
    )
    session.add(store_setting)
    
    # Create languages
    from models.language import Language
    english = Language(
        name="English",
        code="en",
        flag="/flags/en.png",
        is_default=True,
        is_active=True
    )
    spanish = Language(
        name="Spanish",
        code="es",
        flag="/flags/es.png",
        is_default=False,
        is_active=True
    )
    session.add(english)
    session.add(spanish)
    
    # Commit all changes
    session.commit()
    session.close()
    
    print("Sample data created successfully")

if __name__ == "__main__":
    # No confirmation, just run
    update_database()
