"""Logging configuration for all services."""
import logging
import sys
from typing import Optional

from .env_variables import LOG_LEVEL, ENV


def setup_logging(service_name: Optional[str] = None) -> logging.Logger:
    """Configure logging for a service."""
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(filename)s:%(lineno)d - %(message)s"
    )

    if ENV in ("local", "docker"):
        log_format = (
            "%(levelname)s:\t  %(message)s"  # Simpler format for development
        )

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    if service_name:
        logger = logging.getLogger(service_name)
    else:
        logger = logging.getLogger(__name__)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
