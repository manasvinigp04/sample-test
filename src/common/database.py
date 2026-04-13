"""Database configuration and utilities."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool

from .env_variables import DATABASE_URL, ENV


# Create async engine
# Use StaticPool for SQLite to avoid threading issues
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
poolclass = StaticPool if "sqlite" in DATABASE_URL else None

engine = create_async_engine(
    DATABASE_URL,
    echo=ENV == "local",  # Log SQL queries in local environment
    connect_args=connect_args,
    poolclass=poolclass,
    pool_pre_ping=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for all models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database - create all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connection."""
    await engine.dispose()
