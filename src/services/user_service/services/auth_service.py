"""Authentication service for JWT and password management."""
from datetime import datetime, timedelta
from typing import Optional

from src.common.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    get_token_expiry
)
from src.common.exceptions import AuthenticationError
from src.common.env_variables import JWT_EXPIRATION_MINUTES
from ..models.domain import TokenData
from ..repository import UserSessionRepository


class AuthService:
    """Authentication service."""

    def __init__(self, session_repo: UserSessionRepository):
        self.session_repo = session_repo

    def hash_password(self, password: str) -> str:
        """Hash a password."""
        return hash_password(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password."""
        return verify_password(plain_password, hashed_password)

    async def create_token(self, user_id: int, username: str, role: str) -> str:
        """Create JWT token and store session."""
        token = create_access_token(
            data={"sub": str(user_id), "username": username, "role": role}
        )

        # Decode to get JTI and expiry
        payload = decode_access_token(token)
        token_jti = payload["jti"]
        expires_at = datetime.fromtimestamp(payload["exp"])

        # Store session
        await self.session_repo.create_session(user_id, token_jti, expires_at)

        return token

    async def verify_token(self, token: str) -> TokenData:
        """Verify JWT token and check session."""
        try:
            payload = decode_access_token(token)
        except AuthenticationError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")

        # Check if session exists
        token_jti = payload.get("jti")
        if not token_jti:
            raise AuthenticationError("Invalid token: missing JTI")

        session = await self.session_repo.get_by_jti(token_jti)
        if not session:
            raise AuthenticationError("Token session not found or expired")

        # Check if session expired
        if session.expires_at < datetime.utcnow():
            await self.session_repo.delete_session(token_jti)
            raise AuthenticationError("Token expired")

        # Extract user info
        user_id = int(payload.get("sub"))
        username = payload.get("username")
        role = payload.get("role")

        return TokenData(user_id=user_id, username=username, role=role)

    async def invalidate_token(self, token: str) -> bool:
        """Invalidate a token (logout)."""
        try:
            payload = decode_access_token(token)
            token_jti = payload.get("jti")
            if token_jti:
                return await self.session_repo.delete_session(token_jti)
        except AuthenticationError:
            pass
        return False

    async def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions."""
        return await self.session_repo.delete_expired_sessions()
