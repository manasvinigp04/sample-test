"""Constants for service URLs and other configuration."""
import os
from typing import Dict

from .env_variables import ENV


# Service URLs (for Docker internal network)
_SERVICE_URLS_DOCKER: Dict[str, str] = {
    "user": "http://user_service:8001",
    "product": "http://product_service:8002",
    "order": "http://order_service:8003",
    "payment": "http://payment_service:8004",
}

# Service URLs (for local development)
_SERVICE_URLS_LOCAL: Dict[str, str] = {
    "user": "http://localhost:8001",
    "product": "http://localhost:8002",
    "order": "http://localhost:8003",
    "payment": "http://localhost:8004",
}

# Select URLs based on environment
SERVICE_URLS = _SERVICE_URLS_DOCKER if ENV == "docker" else _SERVICE_URLS_LOCAL

USER_SERVICE_URL = SERVICE_URLS["user"]
PRODUCT_SERVICE_URL = SERVICE_URLS["product"]
ORDER_SERVICE_URL = SERVICE_URLS["order"]
PAYMENT_SERVICE_URL = SERVICE_URLS["payment"]

# HTTP Timeouts (in seconds)
DEFAULT_TIMEOUT = 30
CONNECT_TIMEOUT = 5
READ_TIMEOUT = 25

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Product Categories
PRODUCT_CATEGORIES = ["electronics", "clothing", "books", "home"]

# Order Statuses
ORDER_STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"]

# Payment Methods
PAYMENT_METHODS = ["credit_card", "debit_card", "paypal", "stripe"]

# Payment Statuses
PAYMENT_STATUSES = ["pending", "completed", "failed", "refunded"]

# Transaction Types
TRANSACTION_TYPES = ["charge", "refund"]

# User Roles
USER_ROLES = ["customer", "admin"]
