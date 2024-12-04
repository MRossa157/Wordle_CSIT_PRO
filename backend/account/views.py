from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends

from backend.account.schemas import UserInfoResponse
from backend.auth.constants import API_RESPONSES
from backend.auth.dependencies import validate_access_token
from backend.auth.service import get_current_active_auth_user

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
    user = await get_current_active_auth_user(token_payload)

    return UserInfoResponse(
        username=user.username,
    )
