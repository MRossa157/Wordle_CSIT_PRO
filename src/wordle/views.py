from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends

from src.account.schemas import GameSessionResponse, GameSessionsResponse
from src.account.services import create_new_game_session
from src.auth.constants import API_RESPONSES
from src.auth.dependencies import validate_access_token
from src.auth.service import get_current_active_auth_user
from src.wordle.dependencies import validate_word_data
from src.wordle.schemas import WordleRequestCheckWord, WordleResponseCheckWord
from src.wordle.services import check_word_service, get_all_user_gamesessions

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
    user = await get_current_active_auth_user(token_payload)

    session_id = await create_new_game_session(user.id)

    return GameSessionResponse(session_id=session_id)


@router.get(
        path='/game_sessions',
        summary='Получить список всех игровых сессий которые были у пользователя',
)
async def get_game_sessions(
        token_payload: Annotated[
            Dict[str, Any],
            Depends(validate_access_token),
        ],
) -> GameSessionsResponse:
    user = await get_current_active_auth_user(token_payload)

    return GameSessionsResponse(
        user_sessions=await get_all_user_gamesessions(user.id),
    )


@router.post(
    path='/check_word',
    summary='Проверить слово',
)
async def check_word(
        word_data: Annotated[
            WordleRequestCheckWord,
            Depends(validate_word_data),
        ],
) -> WordleResponseCheckWord:
    return await check_word_service(
        session_id=word_data.session_id,
        word=word_data.word,
    )
