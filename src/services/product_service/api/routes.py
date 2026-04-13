"""API routes for Product Service."""
from typing import Annotated, Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query

from ..models.domain import ProductCreate, ProductUpdate, ProductResponse, CategoryResponse
from ..services.product_service import ProductService
from ..repository import ProductRepository
from ..cache import ProductCache
from src.common.database import get_db
from src.common.exceptions import NotFoundError, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


async def get_product_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ProductService:
    """Get product service."""
    repo = ProductRepository(db)
    cache = ProductCache()
    return ProductService(repo, cache)


@router.get("/products", response_model=List[ProductResponse])
async def list_products(
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    service: Annotated[ProductService, Depends(get_product_service)] = None
):
    """List products with optional filters."""
    return await service.list_products(category, min_price)


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    service: Annotated[ProductService, Depends(get_product_service)]
):
    """Create a new product."""
    try:
        return await service.create_product(product_data)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_product_service)]
):
    """Get product by ID."""
    try:
        return await service.get_product(product_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: Annotated[ProductService, Depends(get_product_service)]
):
    """Update a product."""
    try:
        return await service.update_product(product_id, product_data)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_product_service)]
):
    """Delete a product."""
    try:
        await service.delete_product(product_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.get("/categories", response_model=List[CategoryResponse])
async def list_categories(
    service: Annotated[ProductService, Depends(get_product_service)]
):
    """List all categories."""
    return await service.list_categories()
