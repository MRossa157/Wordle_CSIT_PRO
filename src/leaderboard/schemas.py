from typing import List, Optional

from pydantic import BaseModel


class UserStats(BaseModel):
    username: str
    wins_count: int
    w_l: float


class LeaderboardResponse(BaseModel):
    user_stats: Optional[UserStats]
    leaderboard_stats: List[UserStats]
