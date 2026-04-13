"""Authentication utilities for JWT and password management."""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uuid
import hashlib

from jose import JWTError, jwt

from .env_variables import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_MINUTES
from .exceptions import AuthenticationError


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2."""
    salt = hashlib.sha256(password.encode()).digest()
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return hash_password(plain_password) == hashed_password


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4())  # JWT ID for token tracking
    })

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and verify a JWT access token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as e:
        raise AuthenticationError(f"Invalid token: {str(e)}")


def get_token_expiry(token: str) -> Optional[datetime]:
    """Extract expiry time from token."""
    try:
        payload = decode_access_token(token)
        exp = payload.get("exp")
        if exp:
            return datetime.fromtimestamp(exp)
        return None
    except AuthenticationError:
        return None


def get_user_id_from_token(token: str) -> Optional[int]:
    """Extract user ID from token."""
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id:
            return int(user_id)
        return None
    except (AuthenticationError, ValueError):
        return None


def validate_password_strength(password: str) -> bool:
    """Validate password meets minimum requirements."""
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True
