"""Repository layer for Product Service."""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models.database import Product, Category
from src.common.exceptions import NotFoundError


class ProductRepository:
    """Product data access repository."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID."""
        result = await self.db.execute(
            select(Product).where(Product.id == product_id, Product.is_active == True)
        )
        return result.scalar_one_or_none()

    async def list_products(
        self,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        limit: int = 50
    ) -> List[Product]:
        """List products with filters."""
        query = select(Product).where(Product.is_active == True)

        if category:
            # Join with category table
            query = query.join(Category).where(Category.name == category)

        if min_price is not None:
            query = query.where(Product.price >= min_price)

        query = query.limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, product_data: dict) -> Product:
        """Create a new product."""
        # Get or create category
        category_name = product_data.pop("category", None)
        category_id = None

        if category_name:
            category_id = await self._get_or_create_category(category_name)

        product = Product(**product_data, category_id=category_id)
        self.db.add(product)
        await self.db.flush()
        await self.db.refresh(product)
        return product

    async def update(self, product_id: int, product_data: dict) -> Product:
        """Update product."""
        product = await self.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product", product_id)

        # Handle category update
        if "category" in product_data:
            category_name = product_data.pop("category")
            if category_name:
                product.category_id = await self._get_or_create_category(category_name)
            else:
                product.category_id = None

        for key, value in product_data.items():
            setattr(product, key, value)

        await self.db.flush()
        await self.db.refresh(product)
        return product

    async def delete(self, product_id: int) -> bool:
        """Delete product (soft delete)."""
        product = await self.get_by_id(product_id)
        if not product:
            raise NotFoundError("Product", product_id)

        product.is_active = False
        await self.db.flush()
        return True

    async def _get_or_create_category(self, category_name: str) -> int:
        """Get or create category by name."""
        result = await self.db.execute(
            select(Category).where(Category.name == category_name)
        )
        category = result.scalar_one_or_none()

        if not category:
            category = Category(name=category_name)
            self.db.add(category)
            await self.db.flush()
            await self.db.refresh(category)

        return category.id

    async def list_categories(self) -> List[Category]:
        """List all categories."""
        result = await self.db.execute(select(Category))
        return list(result.scalars().all())
