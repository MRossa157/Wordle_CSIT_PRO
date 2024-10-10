from datetime import datetime
from typing import Any, Dict, Optional

from src.utils.database import db_manager


async def add_user(
    username: str,
    password_hash: bytes,
) -> int:
    return await db_manager.pool.fetchval(
        """
        insert into
            users (
                username,
                password_hash,
                created_at
            )
        values
            ($1, $2, $3)
        returning
            id
        """,
        username,
        password_hash,
        datetime.utcnow(),
    )


async def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    return await db_manager.pool.fetchrow(
        """
        select
            *
        from
            users
        where
            username = $1
        """,
        username,
    )


async def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    return await db_manager.pool.fetchrow(
        """
        select
            *
        from
            users
        where
            id = $1
        """,
        user_id,
    )
