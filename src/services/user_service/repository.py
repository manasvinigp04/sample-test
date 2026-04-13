"""Repository layer for User Service data access."""
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models.database import User, UserSession
from src.common.exceptions import NotFoundError, ConflictError


class UserRepository:
    """User data access repository."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: dict) -> User:
        """Create a new user."""
        # Check for existing user
        existing_email = await self.get_by_email(user_data["email"])
        if existing_email:
            raise ConflictError("Email already registered", {"field": "email"})

        existing_username = await self.get_by_username(user_data["username"])
        if existing_username:
            raise ConflictError("Username already taken", {"field": "username"})

        user = User(**user_data)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, user_data: dict) -> User:
        """Update user."""
        user = await self.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)

        # Check email uniqueness if being updated
        if "email" in user_data and user_data["email"] != user.email:
            existing = await self.get_by_email(user_data["email"])
            if existing:
                raise ConflictError("Email already registered", {"field": "email"})

        for key, value in user_data.items():
            setattr(user, key, value)

        user.updated_at = datetime.utcnow()
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        """Delete user (soft delete by marking inactive)."""
        user = await self.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)

        user.is_active = False
        user.updated_at = datetime.utcnow()
        await self.db.flush()
        return True


class UserSessionRepository:
    """User session data access repository."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(
        self,
        user_id: int,
        token_jti: str,
        expires_at: datetime
    ) -> UserSession:
        """Create a new user session."""
        session = UserSession(
            user_id=user_id,
            token_jti=token_jti,
            expires_at=expires_at
        )
        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)
        return session

    async def get_by_jti(self, token_jti: str) -> Optional[UserSession]:
        """Get session by JWT ID."""
        result = await self.db.execute(
            select(UserSession).where(UserSession.token_jti == token_jti)
        )
        return result.scalar_one_or_none()

    async def delete_session(self, token_jti: str) -> bool:
        """Delete a session (logout)."""
        session = await self.get_by_jti(token_jti)
        if session:
            await self.db.delete(session)
            await self.db.flush()
            return True
        return False

    async def delete_expired_sessions(self) -> int:
        """Delete all expired sessions."""
        result = await self.db.execute(
            select(UserSession).where(UserSession.expires_at < datetime.utcnow())
        )
        sessions = result.scalars().all()
        count = len(sessions)
        for session in sessions:
            await self.db.delete(session)
        await self.db.flush()
        return count
