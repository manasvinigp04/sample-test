"""Redis caching for products."""
from typing import Optional

from src.common.redis_client import redis_client
from ..models.domain import ProductResponse


class ProductCache:
    """Product caching layer."""

    def __init__(self):
        self.client = redis_client
        self.prefix = "product:"

    def _get_key(self, product_id: int) -> str:
        """Get cache key for product."""
        return f"{self.prefix}{product_id}"

    async def get_product(self, product_id: int) -> Optional[ProductResponse]:
        """Get product from cache."""
        key = self._get_key(product_id)
        data = await self.client.get(key)
        if data:
            return ProductResponse(**data)
        return None

    async def set_product(self, product_id: int, product: ProductResponse) -> bool:
        """Set product in cache."""
        key = self._get_key(product_id)
        data = product.model_dump(mode='json')
        return await self.client.set(key, data)

    async def delete_product(self, product_id: int) -> bool:
        """Delete product from cache."""
        key = self._get_key(product_id)
        return await self.client.delete(key)

    async def clear_all(self) -> int:
        """Clear all product cache."""
        pattern = f"{self.prefix}*"
        return await self.client.delete_pattern(pattern)
