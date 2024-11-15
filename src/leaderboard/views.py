from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends

from src.auth.dependencies import validate_access_token
from src.auth.service import get_current_active_auth_user
from src.leaderboard.schemas import LeaderboardResponse
from src.leaderboard.services import get_leaderboard_info

router = APIRouter()


@router.get(
        path='/',
        summary=(
            'Получить данные по таблице лидеров'
        ),
)
async def get_game_sessions(
        token_payload: Annotated[
            Dict[str, Any],
            Depends(validate_access_token),
        ],
        top_n: int = 20,  # default top 10
) -> LeaderboardResponse:
    user = await get_current_active_auth_user(token_payload)

    return await get_leaderboard_info(user_id=user.id, top_n=top_n)
