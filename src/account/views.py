from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from src.account.schemas import GameSessionResponse, UserInfo, UserInfoResponse
from src.account.services import create_new_game_session
from src.auth.constants import API_RESPONSES
from src.auth.dependencies import validate_access_token
from src.auth.exceptions import HTTP400BadRequest
from src.auth.service import get_current_active_auth_user
from src.auth.utils import username_check
from src.utils.models.models import User

router = APIRouter()


@router.get(
        path='/user_information',
        summary='Получить информацию об авторизованном пользователе',
        responses={
            **API_RESPONSES['user_account'],
        },
)
async def get_authenticated_user_info(
        token_payload: Annotated[
            Dict[str, Any],
            Depends(validate_access_token),
        ],
) -> UserInfoResponse:
    user: User = await get_current_active_auth_user(token_payload)

    return UserInfoResponse(
        username=user.username,
    )


@router.post(
        path='/create_game_session',
        summary='Создать новую игровую сессию',
        responses={
            **API_RESPONSES['create_game_session'],
        },
)
async def create_game_session(
        token_payload: Annotated[
            Dict[str, Any],
            Depends(validate_access_token),
        ],
) -> GameSessionResponse:
    user: User = await get_current_active_auth_user(token_payload)

    session_id = await create_new_game_session(user.id)

    return GameSessionResponse(session_id=session_id)
