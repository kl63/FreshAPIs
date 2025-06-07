from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database.database import Base

# This file will contain common model functionality or base model classes
class TimestampMixin:
    """Mixin that adds created_at and updated_at columns to models"""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
