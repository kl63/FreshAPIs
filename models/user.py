from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database.database import Base
from models.base import TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"
