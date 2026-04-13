"""Product Service - FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.common.database import init_db, close_db
from src.common.redis_client import redis_client
from src.common.logging_config import setup_logging
from src.common.env_variables import ENABLE_SWAGGER_UI
from .api.routes import router


logger = setup_logging("product_service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management."""
    logger.info("Starting Product Service...")
    await init_db()
    await redis_client.connect()
    logger.info("Database and Redis initialized")
    yield
    logger.info("Shutting down Product Service...")
    await redis_client.close()
    await close_db()


app = FastAPI(
    title="Product Service",
    description="Product catalog and inventory management microservice",
    version="1.0.0",
    docs_url="/docs" if ENABLE_SWAGGER_UI else None,
    redoc_url="/redoc" if ENABLE_SWAGGER_UI else None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, tags=["products"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "product_service",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
