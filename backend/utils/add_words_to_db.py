import asyncio

from asyncpg import create_pool

from backend.config import settings


async def load_words_from_file(file_path: str) -> None:
    pool = await create_pool(
        host=settings.DATABASE_HOST,
        port=int(settings.DATABASE_PORT),
        database=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
    )

    with open(file_path) as file:  # noqa: ASYNC230
        words = [line.strip() for line in file if line.strip()]

    async with pool.acquire() as connection, connection.transaction():
        await connection.executemany(
            'INSERT INTO words (word) VALUES ($1) ON CONFLICT DO NOTHING;',
            [(word,) for word in words],
        )

    # Закрываем пул после завершения вставки
    await pool.close()


if __name__ == '__main__':
    filepath = 'wordle-bank.txt'
    asyncio.run(load_words_from_file(file_path=filepath))
