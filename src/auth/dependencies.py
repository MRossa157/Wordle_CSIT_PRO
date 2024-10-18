# ruff: noqa: S106, S105

from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import Request, Response
from jwt.exceptions import InvalidTokenError

from src.auth.config import auth_config
from src.auth.constants import TokenType
from src.auth.crud import (
    get_user_by_username,
)
from src.auth.exceptions import (
    HTTP400BadRequest,
    HTTP401Unauthorized,
)
from src.auth.schemas import UserRegistration
from src.auth.security import OAuth2PasswordBearerWithCookie
from src.auth.service import (
    get_remove_tokens_headers,
)
from src.auth.utils import decode_jwt, password_check, username_check

oauth2_scheme = OAuth2PasswordBearerWithCookie(token_url='/auth/tokens')


async def validate_user_creation(
        user_data: UserRegistration,
) -> UserRegistration:
    if not username_check(user_data.username):
        raise HTTP400BadRequest(detail='Invalid username')

    if not password_check(user_data.password):
        raise HTTP400BadRequest(
            detail='The entered password doesn\'t meet strength requirements',
        )

    if await get_user_by_username(user_data.username):
        raise HTTP400BadRequest(detail='Username already exists')

    return user_data


async def get_current_token_decoded(
        request: Request,
        token_type: str,
) -> Dict[str, Any]:
    token = await oauth2_scheme(request, token_type=token_type)

    try:
        token_payload: Dict[str, Any] = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTP401Unauthorized(detail='Invalid token') from e

    return {
        'token': token,
        'payload': token_payload,
    }


async def validate_access_token(
        request: Request,
) -> Dict[str, Any]:

    decoded_token = await get_current_token_decoded(
        request=request,
        token_type=TokenType.ACCESS,
    )
    token_payload = decoded_token.get('payload')

    current_time = datetime.utcnow()
    time = current_time + timedelta(minutes=auth_config.access_token_exp_mins)

    if time > datetime.fromtimestamp(token_payload.get('exp')):
        raise HTTP401Unauthorized(detail='Invalid token type')

    token_type: str | None = token_payload.get('type')

    if token_type == 'access':
        return token_payload

    raise HTTP401Unauthorized(detail='Invalid token type')


async def validate_refresh_token(
        request: Request,
        response: Response,
) -> Dict[str, Any]:
    try:
        decoded_token = await get_current_token_decoded(
            request=request,
            token_type=TokenType.REFRESH,
        )
    except HTTP401Unauthorized:
        raise HTTP401Unauthorized(
            detail='Invalid refresh token',
            headers=get_remove_tokens_headers(response),
        )

    token_payload: Dict[str, Any] | None = decoded_token.get('payload')
    token_type: str | None = token_payload.get('type')

    if token_type == 'refresh':
        refresh_token: str | None = decoded_token.get('token')

        if refresh_token:
            return token_payload

    raise HTTP401Unauthorized(
        detail='Invalid token type for refresh',
        headers=get_remove_tokens_headers(response),
    )
