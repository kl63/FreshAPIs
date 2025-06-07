from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base
from models.base import TimestampMixin

class Attribute(Base, TimestampMixin):
    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationship with attribute values
    values = relationship("AttributeValue", back_populates="attribute", cascade="all, delete-orphan")

class AttributeValue(Base, TimestampMixin):
    __tablename__ = "attribute_values"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    attribute_id = Column(Integer, ForeignKey("attributes.id", ondelete="CASCADE"))
    is_active = Column(Boolean, default=True)
    
    # Relationship with attribute
    attribute = relationship("Attribute", back_populates="values")
