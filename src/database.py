from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.config import DBSettings
from src.constants import DATABASE_URL

db_settings = DBSettings()
database_url = DATABASE_URL.format(
    DB_USER=db_settings.DATABASE_USER,
    DB_PASS=db_settings.DATABASE_PASSWORD,
    DB_HOST=db_settings.DATABASE_HOST,
    DB_PORT=db_settings.DATABASE_PORT,
    DB_NAME=db_settings.DATABASE_NAME,
)
Base = declarative_base()
metadata = MetaData()

engine = create_async_engine(database_url, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
