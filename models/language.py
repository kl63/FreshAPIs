from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import relationship

from database.database import Base
from models.base import TimestampMixin

class Language(Base, TimestampMixin):
    __tablename__ = "languages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  # e.g. "English", "Spanish"
    code = Column(String(10), unique=True, nullable=False)  # e.g. "en", "es"
    flag = Column(String(100), nullable=True)  # URL to flag image
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Language {self.name}>"
