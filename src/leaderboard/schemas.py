from typing import List

from pydantic import BaseModel


class UserStats(BaseModel):
    username: str
    wins_count: int
    w_l: float


class LeaderboardResponse(BaseModel):
    user_stats: UserStats
    leaderboard_stats: List[UserStats]
