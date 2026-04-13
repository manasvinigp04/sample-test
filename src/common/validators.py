"""Shared validators for the e-commerce application."""
import re
from typing import Optional

from .constants import (
    PRODUCT_CATEGORIES,
    ORDER_STATUSES,
    PAYMENT_METHODS,
    PAYMENT_STATUSES,
    USER_ROLES
)
from .exceptions import ValidationError


def validate_email(email: str) -> str:
    """Validate email format."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValidationError("Invalid email format")
    return email.lower()


def validate_product_category(category: Optional[str]) -> Optional[str]:
    """Validate product category."""
    if category and category not in PRODUCT_CATEGORIES:
        raise ValidationError(
            f"Invalid category. Must be one of: {', '.join(PRODUCT_CATEGORIES)}"
        )
    return category


def validate_order_status(status: str) -> str:
    """Validate order status."""
    if status not in ORDER_STATUSES:
        raise ValidationError(
            f"Invalid order status. Must be one of: {', '.join(ORDER_STATUSES)}"
        )
    return status


def validate_payment_method(method: str) -> str:
    """Validate payment method."""
    if method not in PAYMENT_METHODS:
        raise ValidationError(
            f"Invalid payment method. Must be one of: {', '.join(PAYMENT_METHODS)}"
        )
    return method


def validate_payment_status(status: str) -> str:
    """Validate payment status."""
    if status not in PAYMENT_STATUSES:
        raise ValidationError(
            f"Invalid payment status. Must be one of: {', '.join(PAYMENT_STATUSES)}"
        )
    return status


def validate_user_role(role: str) -> str:
    """Validate user role."""
    if role not in USER_ROLES:
        raise ValidationError(
            f"Invalid user role. Must be one of: {', '.join(USER_ROLES)}"
        )
    return role


def validate_price(price: float) -> float:
    """Validate price is within acceptable range."""
    if price < 0:
        raise ValidationError("Price cannot be negative")
    if price > 1000000:
        raise ValidationError("Price cannot exceed 1,000,000")
    return round(price, 2)


def validate_stock(stock: int) -> int:
    """Validate stock quantity."""
    if stock < 0:
        raise ValidationError("Stock cannot be negative")
    return stock


def validate_quantity(quantity: int) -> int:
    """Validate order quantity."""
    if quantity < 1:
        raise ValidationError("Quantity must be at least 1")
    if quantity > 100:
        raise ValidationError("Quantity cannot exceed 100")
    return quantity


def validate_shipping_address(address: str) -> str:
    """Validate shipping address length."""
    if len(address) < 10:
        raise ValidationError("Shipping address must be at least 10 characters")
    if len(address) > 500:
        raise ValidationError("Shipping address cannot exceed 500 characters")
    return address.strip()


def validate_product_name(name: str) -> str:
    """Validate product name."""
    name = name.strip()
    if len(name) < 1:
        raise ValidationError("Product name cannot be empty")
    if len(name) > 200:
        raise ValidationError("Product name cannot exceed 200 characters")
    return name


def validate_username(username: str) -> str:
    """Validate username format."""
    username = username.strip()
    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters")
    if len(username) > 50:
        raise ValidationError("Username cannot exceed 50 characters")
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValidationError("Username can only contain letters, numbers, hyphens, and underscores")
    return username
