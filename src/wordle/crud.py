from datetime import datetime
from uuid import UUID

from src.utils.database import db_manager


async def get_word_by_id(word_id: int) -> int:
    return await db_manager.pool.fetchval(
        """
        select
            word
        from
            words
        where
            id = $1
        """,
        word_id,
    )


async def get_game_session_word_id(session_id: UUID) -> int:
    return await db_manager.pool.fetchval(
        """
        select
            guess_word_id
        from
            game_sessions
        where
            session_id = $1
        """,
        session_id,
    )