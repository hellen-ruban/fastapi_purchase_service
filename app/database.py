from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.models import Base

DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/magic_shop"
)

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def reset_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)