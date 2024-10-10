# ruff: noqa: ARG001

import uuid
from typing import Annotated, Any, Dict

from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response,
    status,
)
from starlette.responses import JSONResponse

from src.auth.constants import API_RESPONSES
from src.auth.dependencies import validate_refresh_token, validate_user_creation
from src.auth.schemas import (
    JWTResponse,
    UserAuthentication,
    UserRegistration,
    ValidatedUserAuthentication,
)
from src.auth.service import (
    auth_user,
    confirm_user,
    get_access_refresh_tokens,
    get_current_active_auth_user,
    remove_access_refresh_tokens,
)

router = APIRouter()


@router.post(
        path='/register',
        status_code=status.HTTP_201_CREATED,
        summary='Зарегистрировать пользователя',
        responses={
            **API_RESPONSES['register'],
        },
)
async def register_user(
        user_data: Annotated[
            UserRegistration,
            Depends(validate_user_creation),
        ],
) -> None:
    await confirm_user(
        user_data=user_data,
    )


@router.post(
        path='/login',
        response_model=JWTResponse,
        summary='Авторизовать существующего пользователя',
        responses={
            **API_RESPONSES['login'],
        },
)
async def authorize_user(
        request: Request,
        response: Response,
        auth_data: UserAuthentication,
) -> JWTResponse:
    user: ValidatedUserAuthentication = await auth_user(auth_data)

    device_id = request.cookies.get('device_id')

    if not device_id:
        device_id = str(uuid.uuid4())
        response.set_cookie(
            key='device_id',
            value=device_id,
            httponly=True,
            max_age=31536000,
        )

    return get_access_refresh_tokens(
        response=response,
        user_id=user.id,
    )


@router.put(
        path='/tokens',
        response_model=JWTResponse,
        response_model_exclude_none=True,
        summary='Обновить access token пользователя',
        responses={
            **API_RESPONSES['tokens'],
        },
)
async def refresh_access_token(
        request: Request,
        response: Response,
        token_payload: Annotated[
            Dict[str, Any],
            Depends(validate_refresh_token),
        ],
) -> JWTResponse:
    user: Dict[str, Any] = await get_current_active_auth_user(token_payload)
    device_id = request.cookies.get('device_id')

    return get_access_refresh_tokens(
        response=response,
        user_id=user.get('id'),
        device_id=device_id,
    )


@router.put(
        path='/tokens/check',
        response_class=JSONResponse,
        summary='Проверить валидность refresh токена',
        responses={
            **API_RESPONSES['check_tokens'],
        },
        include_in_schema=False,
)
async def check_tokens(
        request: Request,
        response: Response,
        token_payload: Annotated[
            Dict[str, Any],
            Depends(validate_refresh_token),
        ],
) -> JSONResponse:
    return JSONResponse(content={'message': 'Refresh token is valid'})


@router.post(
        path='/logout',
        response_model=JWTResponse,
        summary='Выйти из личного кабинета пользователя',
        responses={
            **API_RESPONSES['logout'],
        },
)
async def logout(
        response: Response,
        token_payload: Annotated[
            Dict[str, Any],
            Depends(validate_refresh_token),
        ],
) -> JWTResponse:
    return remove_access_refresh_tokens(response)
