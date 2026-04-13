"""Pydantic models for User Service API."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator

from src.common.validators import validate_username
from src.common.auth import validate_password_strength
from src.common.constants import USER_ROLES


class UserBase(BaseModel):
    """Base user fields."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)

    @validator('username')
    def username_validator(cls, v):
        return validate_username(v)


class UserCreate(UserBase):
    """User creation request."""

    password: str = Field(..., min_length=8, max_length=100)

    @validator('password')
    def password_validator(cls, v):
        if not validate_password_strength(v):
            raise ValueError(
                "Password must contain at least 8 characters, "
                "including uppercase, lowercase, and a number"
            )
        return v


class UserUpdate(BaseModel):
    """User update request."""

    full_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """User response."""

    id: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Login request."""

    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response with access token."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token payload data."""

    user_id: int
    username: str
    role: str
