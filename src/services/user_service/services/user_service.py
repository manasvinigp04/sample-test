"""User service business logic."""
from typing import Optional

from ..models.domain import UserCreate, UserUpdate, UserResponse, LoginRequest, LoginResponse
from ..models.database import User
from ..repository import UserRepository
from .auth_service import AuthService
from src.common.exceptions import AuthenticationError, NotFoundError


class UserService:
    """User business logic service."""

    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """Register a new user."""
        # Hash password
        password_hash = self.auth_service.hash_password(user_data.password)

        # Create user
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["password_hash"] = password_hash
        user_dict["role"] = "customer"  # Default role

        user = await self.user_repo.create(user_dict)
        return UserResponse.model_validate(user)

    async def login(self, login_data: LoginRequest) -> LoginResponse:
        """Authenticate user and return token."""
        # Get user by username
        user = await self.user_repo.get_by_username(login_data.username)
        if not user:
            raise AuthenticationError("Invalid username or password")

        # Verify password
        if not self.auth_service.verify_password(login_data.password, user.password_hash):
            raise AuthenticationError("Invalid username or password")

        # Check if user is active
        if not user.is_active:
            raise AuthenticationError("User account is disabled")

        # Create token
        token = await self.auth_service.create_token(user.id, user.username, user.role)

        return LoginResponse(
            access_token=token,
            user=UserResponse.model_validate(user)
        )

    async def logout(self, token: str) -> bool:
        """Logout user by invalidating token."""
        return await self.auth_service.invalidate_token(token)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """Get user by ID."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """Update user profile."""
        update_dict = user_data.model_dump(exclude_unset=True)
        if not update_dict:
            # Nothing to update
            return await self.get_user_by_id(user_id)

        user = await self.user_repo.update(user_id, update_dict)
        return UserResponse.model_validate(user)

    async def delete_user(self, user_id: int) -> bool:
        """Delete user account."""
        return await self.user_repo.delete(user_id)
