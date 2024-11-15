import json
from datetime import datetime
from typing import List
from uuid import UUID

from src.utils.database import db_manager
from src.wordle.dtos import GameSessionInfo, UserGameSession


async def get_word_id_by_word(word: str) -> int:
    return await db_manager.pool.fetchval(
        """
        select
            id
        from
            words
        where
            word = $1
        """,
        word,
    )


async def check_game_session_exists(session_id: UUID) -> bool:
    return await db_manager.pool.fetchval(
        """
        select exists (
            select
                1
            from
                game_sessions
            where
                session_id = $1 and finished_at is NULL
        )
        """,
        session_id,
    )


async def get_game_sessions_by_user_id(
        user_id: int,
) -> List[UserGameSession]:
    result = await db_manager.pool.fetch(
        """
        select
            gs.session_id,
            gs.game_state,
            coalesce(
                jsonb_object_agg(ga.attempt_number, ga.attempt_word)
                FILTER (where ga.attempt_number is NOT NULL),
                '{}'::jsonb
            ) as attempts_info
        from
            game_sessions gs
        left join
            game_attempts ga ON gs.session_id = ga.session_id
        where
            gs.owner_id = $1
        group by
            gs.session_id, gs.game_state
        order by
            gs.created_at desc
        """,
        user_id,
    )
    return [
        UserGameSession(
            session_id=row['session_id'],
            game_state=row['game_state'],
            attempts_info={
            int(key): value
            for key, value in json.loads(row['attempts_info']).items()
        },
        )
        for row in result
    ]


async def get_game_session_info_by_session_id(
    session_id: UUID,
) -> GameSessionInfo:
    result = await db_manager.pool.fetchrow(
        """
        select
            gs.session_id,
            gs.owner_id,
            gs.created_at,
            gs.finished_at,
            w.word,
            coalesce(
                jsonb_object_agg(ga.attempt_number, ga.attempt_word)
                FILTER (where ga.attempt_number is NOT NULL),
                '{}'::jsonb
            ) as attempts_info
        from
            game_sessions gs
        left join
            words w ON gs.guess_word_id = w.id
        left join
            game_attempts ga ON gs.session_id = ga.session_id
        where
            gs.session_id = $1
        group by
            gs.session_id, gs.owner_id, gs.created_at, gs.finished_at, w.word
        """,
        session_id,
    )
    return GameSessionInfo(
        session_id=result['session_id'],
        owner_id=result['owner_id'],
        created_at=result['created_at'],
        finished_at=result['finished_at'],
        word=result['word'],
        attempts_info={
            int(key): value
            for key, value in json.loads(result['attempts_info']).items()
        },
    )


async def add_attempt(
        session_id: UUID,
        owner_id: int,
        created_at: datetime,
        attempt_number: int,
        word: str,
) -> None:
    return await db_manager.pool.execute(
        """
        insert into
            game_attempts (
                session_id,
                owner_id,
                created_at,
                attempt_number,
                attempt_word
            )
        values
            ($1, $2, $3, $4, $5)
        """,
        session_id,
        owner_id,
        created_at,
        attempt_number,
        word,
    )


async def finish_game_by_session_id(
        session_id: UUID,
        finished_at: datetime,
        game_state: str,
) -> None:
    return await db_manager.pool.execute(
        """
        update
            game_sessions
        set
            finished_at = $2,
            game_state = $3
        where
            session_id = $1
        """,
        session_id,
        finished_at,
        game_state,
    )


async def remove_not_used_game_sessions() -> None:
    return await db_manager.pool.execute(
        """
        delete from
            game_sessions
        where
            created_at <= now() at time zone 'UTC' - interval '1 hour'
            and not exists(
                select
                    1
                from
                    game_attempts
                where
                    game_attempts.session_id = game_sessions.session_id
            )
            and finished_at is null
            and game_state = 'IN_PROGRESS'
         """,
    )
