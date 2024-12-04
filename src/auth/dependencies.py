# ruff: noqa: S106, S105

from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import Request, Response
from jwt.exceptions import InvalidTokenError

from src.auth.constants import token_types
from src.auth.crud import (
    get_user_by_username,
)
from src.auth.exceptions import HTTP401Unauthorized
from src.auth.schemas import UserRegistration
from src.auth.security import OAuth2PasswordBearerWithCookie
from src.auth.service import (
    get_access_refresh_tokens,
    get_current_active_auth_user,
    get_remove_tokens_headers,
)
from src.auth.utils import decode_jwt, password_check, username_check
from src.exceptions import HTTP400BadRequest

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
        response: Response,
        token_type: str,
) -> Dict[str, Any]:
    try:
        token = await oauth2_scheme(request, token_type=token_type)
        token_payload: Dict[str, Any] = decode_jwt(token)
        return {
            'token': token,
            'payload': token_payload,
        }
    except InvalidTokenError:
        if token_type != token_types.ACCESS:
            raise HTTP401Unauthorized(detail='Invalid token')
    try:
        new_token_payload = await refresh_access_token(request, response)
        return {
            'payload': new_token_payload,
        }
    except InvalidTokenError:
        raise HTTP401Unauthorized(detail='Invalid token')


async def validate_access_token(
        request: Request,
        response: Response,
) -> Optional[Dict[str, Any]]:
    try:
        decoded_token = await get_current_token_decoded(
            request=request,
            response=response,
            token_type=token_types.ACCESS,
        )
    except HTTP401Unauthorized:
        return None

    token_payload: Dict[str, Any] = decoded_token.get('payload')

    current_time = datetime.utcnow()

    if current_time >= datetime.fromtimestamp(token_payload.get('exp')):
        raise HTTP401Unauthorized(detail='Invalid token type')

    if token_payload.get('type') == 'access':
        return token_payload

    raise HTTP401Unauthorized(detail='Invalid token type')


async def validate_refresh_token(
        request: Request,
        response: Response,
) -> Dict[str, Any]:
    try:
        decoded_token = await get_current_token_decoded(
            request=request,
            response=response,
            token_type=token_types.REFRESH,
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


async def refresh_access_token(
        request: Request,
        response: Response,
) -> Dict | None:
    token_payload = await validate_refresh_token(request, response)
    user: Dict[str, Any] = await get_current_active_auth_user(token_payload)

    new_tokens = get_access_refresh_tokens(
        response=response,
        user_id=user.id,
        is_remembered=True,
    )

    return decode_jwt(new_tokens.access_token)
