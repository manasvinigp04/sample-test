"""Product Service with Redis caching."""
from typing import List, Optional

from ..models.domain import ProductCreate, ProductUpdate, ProductResponse, CategoryResponse
from ..repository import ProductRepository
from ..cache import ProductCache
from src.common.exceptions import NotFoundError, InsufficientStockError


class ProductService:
    """Product business logic service."""

    def __init__(self, product_repo: ProductRepository, cache: ProductCache):
        self.product_repo = product_repo
        self.cache = cache

    async def get_product(self, product_id: int) -> ProductResponse:
        """Get product by ID with caching."""
        # Try cache first
        cached = await self.cache.get_product(product_id)
        if cached:
            return cached

        # Get from database
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product", product_id)

        response = ProductResponse.model_validate(product)

        # Cache it
        await self.cache.set_product(product_id, response)

        return response

    async def list_products(
        self,
        category: Optional[str] = None,
        min_price: Optional[float] = None
    ) -> List[ProductResponse]:
        """List products with filters."""
        products = await self.product_repo.list_products(category, min_price)
        return [ProductResponse.model_validate(p) for p in products]

    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """Create a new product."""
        product_dict = product_data.model_dump()
        product = await self.product_repo.create(product_dict)
        return ProductResponse.model_validate(product)

    async def update_product(
        self,
        product_id: int,
        product_data: ProductUpdate
    ) -> ProductResponse:
        """Update a product."""
        update_dict = product_data.model_dump(exclude_unset=True)
        if not update_dict:
            return await self.get_product(product_id)

        product = await self.product_repo.update(product_id, update_dict)

        # Invalidate cache
        await self.cache.delete_product(product_id)

        return ProductResponse.model_validate(product)

    async def delete_product(self, product_id: int) -> bool:
        """Delete a product."""
        result = await self.product_repo.delete(product_id)

        # Invalidate cache
        await self.cache.delete_product(product_id)

        return result

    async def check_stock(self, product_id: int, quantity: int) -> bool:
        """Check if sufficient stock is available."""
        product = await self.get_product(product_id)
        if product.stock < quantity:
            raise InsufficientStockError(product_id, quantity, product.stock)
        return True

    async def reserve_stock(self, product_id: int, quantity: int) -> bool:
        """Reserve stock for an order."""
        await self.check_stock(product_id, quantity)

        product = await self.product_repo.get_by_id(product_id)
        product.stock -= quantity
        await self.product_repo.db.flush()

        # Invalidate cache
        await self.cache.delete_product(product_id)

        return True

    async def list_categories(self) -> List[CategoryResponse]:
        """List all categories."""
        categories = await self.product_repo.list_categories()
        return [CategoryResponse.model_validate(c) for c in categories]
