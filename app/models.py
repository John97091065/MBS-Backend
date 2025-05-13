from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String(20))
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    image_url = Column(String(255), nullable=True)
    likes = Column(Integer, default=0)
    category = Column(String(50), nullable=False)