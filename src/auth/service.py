# ruff: noqa: S106

from datetime import timedelta
from typing import Any, Dict, Optional

from fastapi import Response
from starlette.datastructures import MutableHeaders

from src.auth.config import auth_config
from src.auth.constants import TokenType
from src.auth.crud import (
    add_user,
    get_user_by_id,
    get_user_by_username,
)
from src.auth.exceptions import HTTP400BadRequest, HTTP401Unauthorized
from src.auth.schemas import (
    JWTResponse,
    UserAuthentication,
    UserRegistration,
    ValidatedUserAuthentication,
)
from src.auth.utils import (
    encode_jwt,
    hash_password,
    validate_password,
)


async def get_current_active_auth_user(
        token_payload: Dict[str, Any],
) -> Dict[str, Any]:
    user: Dict[str, Any] | None = await get_user_by_id(
        token_payload.get('sub'),
    )

    if not user:
        raise HTTP401Unauthorized(detail='Invalid token')
    return user


async def auth_user(
        user_data: UserAuthentication,
) -> ValidatedUserAuthentication:
    user: Dict[str, Any] | None = await get_user_by_username(user_data.username)

    if not user:
        raise HTTP400BadRequest(detail='Invalid login')

    if not validate_password(user_data.password, user['password_hash']):
        raise HTTP400BadRequest(detail='Invalid password')

    return ValidatedUserAuthentication(
        id=user.get('id'),
        username=user_data.username,
        password=user_data.password,
    )


def create_jwt(
        token_type: str,
        token_data: Dict[str, Any],
        expiration_time: timedelta,
) -> str:
    payload: Dict[str, Any] = {'type': token_type}
    payload.update(token_data)

    return encode_jwt(payload, expiration_time)


def create_access_token(
        user_id: int,
) -> str:
    token_data: Dict[str, Any] = {
        'sub': user_id,
    }
    expiration_time = timedelta(
        minutes=auth_config.access_token_exp_mins,
    )

    return create_jwt(
        token_type='access',
        token_data=token_data,
        expiration_time=expiration_time,
    )


def create_refresh_token(user_id: int) -> str:
    token_data: Dict[str, Any] = {
        'sub': user_id,
    }
    expiration_time = timedelta(
        days=auth_config.refresh_token_exp_days,
    )
    return create_jwt(
        token_type='refresh',
        token_data=token_data,
        expiration_time=expiration_time,
    )


def remove_access_refresh_tokens(
        response: Response,
) -> JWTResponse:
    response.delete_cookie(
        key=TokenType.ACCESS,
        path='/',
    )
    response.delete_cookie(
        key=TokenType.REFRESH,
        path='/',
    )

    return JWTResponse(
        access_token='',
        refresh_token='',
        message='Logged out.',
    )


def get_access_refresh_tokens(
        response: Response,
        user_id: int,
) -> JWTResponse:
    access_token: str = create_access_token(user_id)
    refresh_token: str = create_refresh_token(user_id)

    response.set_cookie(
        key=TokenType.ACCESS,
        value=access_token,
        httponly=True,
    )

    response.set_cookie(
        key=TokenType.REFRESH,
        value=refresh_token,
        httponly=True,
    )

    return JWTResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def confirm_user(
        user_data: UserRegistration,
) -> Optional[int]:
    if user_data:
        return await add_user(
            username=user_data.username,
            password_hash=hash_password(user_data.password),
        )
    return None


def get_remove_tokens_headers(response: Response) -> MutableHeaders:
    response.delete_cookie(
        key=TokenType.ACCESS,
        path='/',
    )
    response.delete_cookie(
        key=TokenType.REFRESH,
        path='/',
    )

    return response.headers
