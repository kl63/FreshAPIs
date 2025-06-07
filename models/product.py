from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base
from models.base import TimestampMixin

class Product(Base, TimestampMixin):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(150), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    discounted_price = Column(Float, default=0)
    stock_quantity = Column(Integer, default=0)
    availability = Column(Boolean, default=True)  # Renamed from is_available to match frontend
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    image_url = Column(String(255), nullable=True)
    unit = Column(String(50), nullable=True, default="piece")  # e.g., kg, piece, dozen
    short_description = Column(String(255), nullable=True)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    
    def __repr__(self):
        return f"<Product {self.name}>"
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage if discounted_price is set"""
        if self.discounted_price > 0 and self.price > 0:
            return int(100 - ((self.discounted_price * 100) / self.price))
        return 0
