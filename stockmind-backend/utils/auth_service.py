"""Authentication service layer."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, Tuple
from models.database_models import User, TokenBlacklist
from utils.auth_jwt import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from datetime import datetime, timedelta
from config import REFRESH_TOKEN_EXPIRE_DAYS
import uuid


class AuthService:
    """Handle user authentication and token management."""

    @staticmethod
    async def register_user(email: str, password: str, full_name: str, session: AsyncSession) -> Optional[User]:
        """Register new user."""
        # Check if user exists
        result = await session.execute(select(User).where(User.email == email))
        if result.scalar_one_or_none():
            return None  # User already exists

        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
            is_active=True,
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def authenticate_user(email: str, password: str, session: AsyncSession) -> Optional[User]:
        """Authenticate user and return user object."""
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    async def generate_token_pair(user_id: str, email: str) -> Tuple[str, str]:
        """Generate access and refresh tokens."""
        access_token = create_access_token(user_id, email)
        refresh_token = create_refresh_token(user_id, email)
        return access_token, refresh_token

    @staticmethod
    async def refresh_access_token(refresh_token: str, session: AsyncSession) -> Optional[Tuple[str, str]]:
        """Refresh access token using refresh token."""
        # Decode refresh token
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        # Check if token is blacklisted
        jti = payload.get("jti")
        result = await session.execute(select(TokenBlacklist).where(TokenBlacklist.token_jti == jti))
        if result.scalar_one_or_none():
            return None  # Token is blacklisted

        # Get user
        user_id = payload.get("sub")
        email = payload.get("email")

        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            return None

        # Generate new tokens
        return await AuthService.generate_token_pair(user_id, email)

    @staticmethod
    async def logout_user(token: str, user_id: str, session: AsyncSession) -> bool:
        """Blacklist token on logout."""
        payload = decode_token(token)
        if not payload:
            return False

        jti = payload.get("jti")
        exp = payload.get("exp")

        if not jti or not exp:
            return False

        # Add to blacklist
        expires_at = datetime.fromtimestamp(exp)
        blacklist_entry = TokenBlacklist(
            id=str(uuid.uuid4()),
            user_id=user_id,
            token_jti=jti,
            expires_at=expires_at,
        )

        session.add(blacklist_entry)
        await session.commit()
        return True

    @staticmethod
    async def verify_token(token: str, session: AsyncSession) -> Optional[dict]:
        """Verify token and check if blacklisted."""
        payload = decode_token(token)
        if not payload:
            return None

        # Check if blacklisted
        jti = payload.get("jti")
        result = await session.execute(select(TokenBlacklist).where(TokenBlacklist.token_jti == jti))
        if result.scalar_one_or_none():
            return None  # Token is blacklisted

        return payload
