from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.constants import DATABASE_URL

database_url = DATABASE_URL.format(
    DB_USER=settings.DATABASE_USER,
    DB_PASS=settings.DATABASE_PASSWORD,
    DB_HOST=settings.DATABASE_HOST,
    DB_PORT=settings.DATABASE_PORT,
    DB_NAME=settings.DATABASE_NAME,
)

engine = create_async_engine(database_url)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
