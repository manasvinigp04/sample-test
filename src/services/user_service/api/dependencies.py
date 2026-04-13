"""API dependencies for User Service."""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database import get_db
from src.common.exceptions import AuthenticationError, AuthorizationError
from ..repository import UserRepository, UserSessionRepository
from ..services import AuthService, UserService
from ..models.domain import TokenData


# Security scheme
security = HTTPBearer()


async def get_user_repository(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserRepository:
    """Get user repository."""
    return UserRepository(db)


async def get_session_repository(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserSessionRepository:
    """Get session repository."""
    return UserSessionRepository(db)


async def get_auth_service(
    session_repo: Annotated[UserSessionRepository, Depends(get_session_repository)]
) -> AuthService:
    """Get auth service."""
    return AuthService(session_repo)


async def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserService:
    """Get user service."""
    return UserService(user_repo, auth_service)


async def get_current_user(
    credentials: Annotated[HTTPAuthCredentials, Depends(security)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> TokenData:
    """Get current authenticated user from token."""
    try:
        token_data = await auth_service.verify_token(credentials.credentials)
        return token_data
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_admin(
    current_user: Annotated[TokenData, Depends(get_current_user)]
) -> TokenData:
    """Require admin role."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
