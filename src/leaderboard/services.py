from typing import Optional

from src.leaderboard.crud import get_leaderboard_stats, get_user_stats
from src.leaderboard.schemas import LeaderboardResponse


async def get_leaderboard_info(
        top_n: int,
        user_id: Optional[int] = None,
) -> LeaderboardResponse:
    """
    Получает таблицу лидеров,
    а так же статистику конкретного пользователя.
    """
    if user_id is None:
        user_stats = None
    else:
        user_stats = await get_user_stats(user_id)
    leaderboard_stats = await get_leaderboard_stats(top_n)

    return LeaderboardResponse(
        user_stats=user_stats,
        leaderboard_stats=leaderboard_stats,
    )
