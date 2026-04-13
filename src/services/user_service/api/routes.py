"""API routes for User Service."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthCredentials

from ..models.domain import (
    UserCreate,
    UserUpdate,
    UserResponse,
    LoginRequest,
    LoginResponse,
    TokenData
)
from ..services import UserService
from .dependencies import (
    get_user_service,
    get_current_user,
    require_admin,
    security
)
from src.common.exceptions import (
    EcommerceException,
    ValidationError,
    ConflictError,
    NotFoundError,
    AuthenticationError
)


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Register a new user."""
    try:
        return await user_service.register_user(user_data)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Login and receive access token."""
    try:
        return await user_service.login(login_data)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/logout")
async def logout(
    credentials: Annotated[HTTPAuthCredentials, Depends(security)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Logout and invalidate token."""
    await user_service.logout(credentials.credentials)
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Get current user profile."""
    try:
        return await user_service.get_user_by_id(current_user.user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_data: UserUpdate,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Update current user profile."""
    try:
        return await user_service.update_user(current_user.user_id, user_data)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    _: Annotated[TokenData, Depends(require_admin)],  # Admin only
    user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Get user by ID (admin only)."""
    try:
        return await user_service.get_user_by_id(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
