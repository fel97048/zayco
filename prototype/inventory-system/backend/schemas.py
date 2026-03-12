from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Category schemas
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Product schemas
class ProductBase(BaseModel):
    name: str
    category_id: int
    barcode: Optional[str] = None
    unit: str = "個"

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    barcode: Optional[str] = None
    unit: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    category: CategoryResponse
    
    class Config:
        from_attributes = True

# Inventory schemas
class InventoryBase(BaseModel):
    quantity: float
    expiry_date: Optional[datetime] = None

class InventoryResponse(InventoryBase):
    id: int
    product_id: int
    product: ProductResponse
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Inventory History schemas
class InventoryHistoryCreate(BaseModel):
    product_id: int
    transaction_type: str  # "購入" or "使用"
    quantity: float

class InventoryHistoryResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    transaction_type: str
    quantity: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Login schema
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str
