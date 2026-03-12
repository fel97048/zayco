from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    inventory_histories = relationship("InventoryHistory", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    products = relationship("Product", back_populates="category")

class UnitType(str, enum.Enum):
    PIECE = "個"
    BOTTLE = "本"
    BAG = "袋"
    ML = "ml"
    GRAM = "g"
    KG = "kg"
    LITER = "L"

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    barcode = Column(String, unique=True, nullable=True)
    unit = Column(String, nullable=False, default="個")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    inventory_histories = relationship("InventoryHistory", back_populates="product")

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False)
    quantity = Column(Float, default=0, nullable=False)
    expiry_date = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    product = relationship("Product", back_populates="inventory")

class TransactionType(str, enum.Enum):
    PURCHASE = "購入"
    USE = "使用"

class InventoryHistory(Base):
    __tablename__ = "inventory_history"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="inventory_histories")
    user = relationship("User", back_populates="inventory_histories")
