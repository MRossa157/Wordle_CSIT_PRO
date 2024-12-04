from typing import List

from backend.leaderboard.constants import NUMBER_PRECISION
from backend.leaderboard.schemas import UserStats
from backend.utils.database import db_manager


async def get_user_stats(user_id: int) -> UserStats:
    result = await db_manager.pool.fetchrow(
        """
        select
            u.username,
            count(case when gs.game_state = 'WIN' then 1 end) as wins_count,
            coalesce(
                nullif(count(case when gs.game_state = 'WIN' then 1 end), 0) * 1.0 /
                nullif(count(case when gs.game_state in ('WIN', 'LOSS') then 1 end), 0),
                0
            ) as "w/l"
        from
            users u
        left join
            game_sessions gs
        on
            gs.owner_id = u.id
        where
            u.id = $1
        group by
            u.username
        """,
        user_id,
    )
    return UserStats(
        username=result['username'],
        wins_count=result['wins_count'],
        w_l=round(result['w/l'], NUMBER_PRECISION),
    )


async def get_leaderboard_stats(top_n: int) -> List[UserStats]:
    result = await db_manager.pool.fetch(
        """
        select
            u.username,
            count(case when gs.game_state = 'WIN' then 1 end) as wins_count,
            coalesce(
                nullif(count(case when gs.game_state = 'WIN' then 1 end), 0) * 1.0 /
                nullif(count(case when gs.game_state in ('WIN', 'LOSS') then 1 end), 0),
                0
            ) as "w/l"
        from
            users u
        left join
            game_sessions gs
        on
            gs.owner_id = u.id
        group by
            u.username
        order by
            "w/l" desc,
            wins_count desc
        limit $1
        """,
        top_n,
    )

    return [
        UserStats(
            username=item['username'],
            wins_count=item['wins_count'],
            w_l=round(item['w/l'], NUMBER_PRECISION),
        )
        for item in result
    ]
