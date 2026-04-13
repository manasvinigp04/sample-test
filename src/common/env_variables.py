"""Environment variables and feature flags for the e-commerce microservices."""
import os
from typing import Optional


# Service Feature Flags
USER_SERVICE_ENABLED = os.getenv("USER_SERVICE_ENABLED", "true").lower() == "true"
PRODUCT_SERVICE_ENABLED = os.getenv("PRODUCT_SERVICE_ENABLED", "true").lower() == "true"
ORDER_SERVICE_ENABLED = os.getenv("ORDER_SERVICE_ENABLED", "true").lower() == "true"
PAYMENT_SERVICE_ENABLED = os.getenv("PAYMENT_SERVICE_ENABLED", "true").lower() == "true"

# Feature Flags
ENABLE_REDIS_CACHE = os.getenv("ENABLE_REDIS_CACHE", "true").lower() == "true"
ENABLE_RATE_LIMITING = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "false").lower() == "true"
ENABLE_SWAGGER_UI = os.getenv("ENABLE_SWAGGER_UI", "true").lower() == "true"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./ecommerce.db")

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "300"))

# JWT Authentication
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production-PLEASE")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))

# Rate Limiting
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_PERIOD_SECONDS = int(os.getenv("RATE_LIMIT_PERIOD_SECONDS", "60"))

# Environment
ENV = os.getenv("ENV", "local")  # local, docker, staging, production

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
