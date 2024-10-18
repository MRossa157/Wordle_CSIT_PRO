from datetime import datetime
from uuid import UUID

from src.utils.database import db_manager


async def get_random_word_id_from_db() -> int:
    return await db_manager.pool.fetchval(
        """
        select
            id
        from
            words
        order by
            random()
        limit
            1
        """,
    )


async def create_game_session(
    session_id: UUID,
    owner_id: int,
    created_at: datetime,
    guess_word_id: int,
) -> UUID:
    await db_manager.pool.execute(
        """
        insert into
            game_sessions (
                session_id,
                owner_id,
                created_at,
                finished_at,
                guess_word_id
            )
        values
            ($1, $2, $3, NULL, $4)
        """,
        session_id,
        owner_id,
        created_at,
        guess_word_id,
    )

    return session_id


async def update_game_session_finish_time(
    session_id: UUID,
    finish_time: datetime,
) -> None:
    return await db_manager.pool.execute(
        """
        update
            game_sessions
        set
            finished_at = $2
        where
            session_id = $1
        """,
        session_id,
        finish_time,
    )
