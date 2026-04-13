"""API Gateway - Main entry point for all services."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

from src.common.constants import USER_SERVICE_URL, PRODUCT_SERVICE_URL
from src.common.logging_config import setup_logging
from src.common.env_variables import ENABLE_SWAGGER_UI


logger = setup_logging("api_gateway")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management."""
    logger.info("Starting API Gateway...")
    yield
    logger.info("Shutting down API Gateway...")


app = FastAPI(
    title="E-commerce API Gateway",
    description="Unified API gateway for e-commerce microservices",
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


async def proxy_request(service_url: str, path: str, request: Request):
    """Proxy request to a microservice."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Forward the request
            response = await client.request(
                method=request.method,
                url=f"{service_url}{path}",
                headers=dict(request.headers),
                params=dict(request.query_params),
                content=await request.body()
            )

            return JSONResponse(
                content=response.json() if response.content else None,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Service unavailable: {service_url}"
            )
        except Exception as e:
            logger.error(f"Proxy error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal gateway error"
            )


# Health check
@app.get("/health")
async def health_check():
    """Gateway health check."""
    return {
        "status": "healthy",
        "service": "api_gateway",
        "version": "1.0.0"
    }


# User Service routes
@app.api_route("/api/v1/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/v1/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def user_service_proxy(path: str, request: Request):
    """Proxy to User Service."""
    # Remove the /api/v1/auth or /api/v1/users prefix
    if path.startswith("auth/"):
        service_path = f"/{path.replace('auth/', '', 1)}"
    elif path.startswith("users/"):
        service_path = f"/{path.replace('users/', '', 1)}"
    else:
        service_path = f"/{path}"

    return await proxy_request(USER_SERVICE_URL, service_path, request)


# Product Service routes
@app.api_route("/api/v1/products/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/api/v1/products", methods=["GET", "POST"])
@app.api_route("/api/v1/categories/{path:path}", methods=["GET"])
@app.api_route("/api/v1/categories", methods=["GET"])
async def product_service_proxy(path: str = "", request: Request = None):
    """Proxy to Product Service."""
    if not request:
        request = path
        path = ""

    service_path = f"/{path}" if path else "/"

    # Handle /api/v1/categories -> /categories
    if "categories" in request.url.path:
        service_path = request.url.path.replace("/api/v1", "")

    # Handle /api/v1/products -> /products
    if "products" in request.url.path:
        service_path = request.url.path.replace("/api/v1", "")

    return await proxy_request(PRODUCT_SERVICE_URL, service_path, request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
