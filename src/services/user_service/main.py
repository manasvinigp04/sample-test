"""User Service - FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.common.database import init_db, close_db
from src.common.logging_config import setup_logging
from src.common.env_variables import ENABLE_SWAGGER_UI
from .api import router


# Setup logging
logger = setup_logging("user_service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management."""
    logger.info("Starting User Service...")
    await init_db()
    logger.info("Database initialized")
    yield
    logger.info("Shutting down User Service...")
    await close_db()


# Create FastAPI app
app = FastAPI(
    title="User Service",
    description="Authentication and user management microservice",
    version="1.0.0",
    docs_url="/docs" if ENABLE_SWAGGER_UI else None,
    redoc_url="/redoc" if ENABLE_SWAGGER_UI else None,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, tags=["auth"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "user_service",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
