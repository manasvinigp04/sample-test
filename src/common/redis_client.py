"""Redis client wrapper for caching."""
import json
import logging
from typing import Any, Optional

import redis.asyncio as redis

from .env_variables import ENABLE_REDIS_CACHE, REDIS_URL, CACHE_TTL_SECONDS


logger = logging.getLogger(__name__)


class RedisClient:
    """Async Redis client wrapper with caching utilities."""

    def __init__(self):
        self.client: Optional[redis.Redis] = None
        self.enabled = ENABLE_REDIS_CACHE

    async def connect(self):
        """Connect to Redis."""
        if not self.enabled:
            logger.info("Redis caching is disabled")
            return

        try:
            self.client = await redis.from_url(
                REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            await self.client.ping()
            logger.info("Connected to Redis successfully")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}. Caching disabled.")
            self.enabled = False
            self.client = None

    async def close(self):
        """Close Redis connection."""
        if self.client:
            await self.client.close()
            logger.info("Redis connection closed")

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.enabled or not self.client:
            return None

        try:
            value = await self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Redis GET error for key {key}: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        if not self.enabled or not self.client:
            return False

        try:
            ttl = ttl or CACHE_TTL_SECONDS
            serialized = json.dumps(value)
            await self.client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.warning(f"Redis SET error for key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.enabled or not self.client:
            return False

        try:
            await self.client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Redis DELETE error for key {key}: {e}")
            return False

    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern."""
        if not self.enabled or not self.client:
            return 0

        try:
            keys = []
            async for key in self.client.scan_iter(match=pattern):
                keys.append(key)
            if keys:
                return await self.client.delete(*keys)
            return 0
        except Exception as e:
            logger.warning(f"Redis DELETE_PATTERN error for pattern {pattern}: {e}")
            return 0

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if not self.enabled or not self.client:
            return False

        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            logger.warning(f"Redis EXISTS error for key {key}: {e}")
            return False


# Global Redis client instance
redis_client = RedisClient()
