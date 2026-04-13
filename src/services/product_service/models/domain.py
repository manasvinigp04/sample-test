"""Pydantic models for Product Service API."""
from datetime import datetime
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field, validator

from src.common.validators import validate_product_name, validate_price, validate_stock, validate_product_category


class ProductBase(BaseModel):
    """Base product fields."""

    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(..., ge=0, le=1000000)
    stock: int = Field(..., ge=0)
    category: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)

    @validator('name')
    def name_validator(cls, v):
        return validate_product_name(v)

    @validator('price')
    def price_validator(cls, v):
        return Decimal(str(validate_price(float(v))))

    @validator('stock')
    def stock_validator(cls, v):
        return validate_stock(v)

    @validator('category')
    def category_validator(cls, v):
        return validate_product_category(v)


class ProductCreate(ProductBase):
    """Product creation request."""
    pass


class ProductUpdate(BaseModel):
    """Product update request."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, ge=0, le=1000000)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)


class ProductResponse(BaseModel):
    """Product response."""

    id: int
    name: str
    description: Optional[str]
    price: Decimal
    stock: int
    category: Optional[str]
    image_url: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    """Category response."""

    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
