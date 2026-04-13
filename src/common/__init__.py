"""Common utilities for e-commerce microservices."""

from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    get_token_expiry,
    get_user_id_from_token,
    validate_password_strength
)
from .constants import (
    USER_SERVICE_URL,
    PRODUCT_SERVICE_URL,
    ORDER_SERVICE_URL,
    PAYMENT_SERVICE_URL,
    SERVICE_URLS,
    DEFAULT_TIMEOUT,
    CONNECT_TIMEOUT,
    READ_TIMEOUT,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    PRODUCT_CATEGORIES,
    ORDER_STATUSES,
    PAYMENT_METHODS,
    PAYMENT_STATUSES,
    USER_ROLES
)
from .database import (
    engine,
    AsyncSessionLocal,
    Base,
    get_db,
    init_db,
    close_db
)
from .exceptions import (
    EcommerceException,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    InsufficientStockError,
    ServiceUnavailableError,
    RateLimitExceededError,
    PaymentError
)
from .logging_config import setup_logging, get_logger
from .redis_client import redis_client, RedisClient
from .validators import (
    validate_email,
    validate_product_category,
    validate_order_status,
    validate_payment_method,
    validate_payment_status,
    validate_user_role,
    validate_price,
    validate_stock,
    validate_quantity,
    validate_shipping_address,
    validate_product_name,
    validate_username
)

__all__ = [
    # Auth
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_access_token",
    "get_token_expiry",
    "get_user_id_from_token",
    "validate_password_strength",
    # Constants
    "USER_SERVICE_URL",
    "PRODUCT_SERVICE_URL",
    "ORDER_SERVICE_URL",
    "PAYMENT_SERVICE_URL",
    "SERVICE_URLS",
    "DEFAULT_TIMEOUT",
    "CONNECT_TIMEOUT",
    "READ_TIMEOUT",
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
    "PRODUCT_CATEGORIES",
    "ORDER_STATUSES",
    "PAYMENT_METHODS",
    "PAYMENT_STATUSES",
    "USER_ROLES",
    # Database
    "engine",
    "AsyncSessionLocal",
    "Base",
    "get_db",
    "init_db",
    "close_db",
    # Exceptions
    "EcommerceException",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ConflictError",
    "InsufficientStockError",
    "ServiceUnavailableError",
    "RateLimitExceededError",
    "PaymentError",
    # Logging
    "setup_logging",
    "get_logger",
    # Redis
    "redis_client",
    "RedisClient",
    # Validators
    "validate_email",
    "validate_product_category",
    "validate_order_status",
    "validate_payment_method",
    "validate_payment_status",
    "validate_user_role",
    "validate_price",
    "validate_stock",
    "validate_quantity",
    "validate_shipping_address",
    "validate_product_name",
    "validate_username",
]
