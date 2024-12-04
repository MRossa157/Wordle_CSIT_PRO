# ruff: noqa: ERA001

from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends

from backend.account.schemas import GameSessionResponse
from backend.account.services import create_new_game_session
from backend.auth.constants import API_RESPONSES
from backend.auth.dependencies import validate_access_token
from backend.auth.service import get_current_active_auth_user
from backend.wordle.dependencies import validate_word_data
from backend.wordle.schemas import (
    WordleRequestCheckWord,
    WordleResponseCheckWord,
    WordleResponseCheckWordFinish,
)
from backend.wordle.services import check_word_service

router = APIRouter()


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
    if token_payload:
        user = await get_current_active_auth_user(token_payload)
        session_id = await create_new_game_session(owner_id=user.id)
    else:
        session_id = await create_new_game_session()

    return GameSessionResponse(session_id=session_id)


# @router.get(
#         path='/game_sessions',
#         summary=(
#             'Получить список всех игровых сессий которые были у пользователя'
#         ),
# )
# async def get_game_sessions(
#         token_payload: Annotated[
#             Dict[str, Any],
#             Depends(validate_access_token),
#         ],
# ) -> GameSessionsResponse:
#     user = await get_current_active_auth_user(token_payload)

#     return GameSessionsResponse(
#         user_sessions=await get_all_user_gamesessions(user.id),
#     )


@router.post(
    path='/check_word',
    summary='Проверить слово',
)
async def check_word(
        word_data: Annotated[
            WordleRequestCheckWord,
            Depends(validate_word_data),
        ],
        token_payload: Annotated[
            Dict[str, Any],
            Depends(validate_access_token),
        ],
) -> WordleResponseCheckWord | WordleResponseCheckWordFinish:
    if token_payload:
        user = await get_current_active_auth_user(token_payload)
        user_id = user.id
    else:
        user_id = None

    return await check_word_service(
        session_id=word_data.session_id,
        word=word_data.word,
        user_id=user_id,
    )
