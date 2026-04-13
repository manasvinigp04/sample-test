"""Custom exceptions for the e-commerce microservices."""
from typing import Any, Dict, Optional


class EcommerceException(Exception):
    """Base exception for e-commerce application."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(EcommerceException):
    """Raised when validation fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class AuthenticationError(EcommerceException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(EcommerceException):
    """Raised when authorization fails."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)


class NotFoundError(EcommerceException):
    """Raised when a resource is not found."""

    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with id={identifier} not found"
        super().__init__(message, status_code=404)


class ConflictError(EcommerceException):
    """Raised when a resource conflict occurs."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=409, details=details)


class InsufficientStockError(ValidationError):
    """Raised when product stock is insufficient."""

    def __init__(self, product_id: int, requested: int, available: int):
        message = f"Insufficient stock for product {product_id}"
        details = {
            "product_id": product_id,
            "requested": requested,
            "available": available
        }
        super().__init__(message, details=details)


class ServiceUnavailableError(EcommerceException):
    """Raised when a dependent service is unavailable."""

    def __init__(self, service: str):
        message = f"{service} service is currently unavailable"
        super().__init__(message, status_code=503)


class RateLimitExceededError(EcommerceException):
    """Raised when rate limit is exceeded."""

    def __init__(self, retry_after: int):
        message = f"Rate limit exceeded. Retry after {retry_after} seconds"
        super().__init__(message, status_code=429, details={"retry_after": retry_after})


class PaymentError(EcommerceException):
    """Raised when payment processing fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=402, details=details)
