from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from database.database import Base
from models.base import TimestampMixin

class Category(Base, TimestampMixin):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Relationships
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    subcategories = relationship("Category", backref=backref("parent", remote_side=[id]))
    
    def __repr__(self):
        return f"<Category {self.name}>"
