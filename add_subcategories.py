from sqlalchemy import create_engine, text
from core.config import settings as app_settings

def add_subcategories():
    """
    Add subcategories to existing categories using raw SQL
    """
    # Create engine
    engine = create_engine(app_settings.DATABASE_URL)
    conn = engine.connect()
    
    try:
        # Get current timestamp for created_at and updated_at fields
        from datetime import datetime
        now = datetime.utcnow().isoformat()
        
        # Define subcategories for Fruits (id=1)
        fruit_subcategories = [
            ("Apples", "apples", "Various types of apples", "/images/categories/apples.png", 1),
            ("Bananas", "bananas", "Fresh bananas", "/images/categories/bananas.png", 1),
            ("Berries", "berries", "All types of berries", "/images/categories/berries.png", 1),
            ("Citrus", "citrus", "Oranges, lemons, and more", "/images/categories/citrus.png", 1),
        ]
        
        # Define subcategories for Vegetables (id=2)
        veg_subcategories = [
            ("Leafy Greens", "leafy-greens", "Spinach, kale, and lettuce", "/images/categories/leafy-greens.png", 2),
            ("Root Vegetables", "root-vegetables", "Carrots, potatoes, and more", "/images/categories/root-vegetables.png", 2),
            ("Onions & Garlic", "onions-garlic", "Flavorful cooking essentials", "/images/categories/onions-garlic.png", 2),
        ]
        
        subcategories = fruit_subcategories + veg_subcategories
        inserted_count = 0
        
        # Insert each subcategory using raw SQL
        for name, slug, description, image_url, parent_id in subcategories:
            sql = text("""
                INSERT INTO categories (name, slug, description, image_url, parent_id, created_at, updated_at) 
                VALUES (:name, :slug, :description, :image_url, :parent_id, :created_at, :updated_at)
            """)
            
            conn.execute(sql, {
                "name": name,
                "slug": slug,
                "description": description,
                "image_url": image_url,
                "parent_id": parent_id,
                "created_at": now,
                "updated_at": now
            })
            inserted_count += 1
        
        # Commit all changes
        conn.commit()
        print(f"Added {inserted_count} subcategories successfully")
    
    finally:
        # Close connection
        conn.close()

if __name__ == "__main__":
    add_subcategories()
