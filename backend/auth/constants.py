from dataclasses import dataclass

from backend.account.schemas import GameSessionResponse, UserInfoResponse
from backend.auth.schemas import JWTResponse


@dataclass(init=False, repr=False, eq=False, frozen=True, match_args=False)
class _TokenType:
    ACCESS: str = 'access_token'
    REFRESH: str = 'refresh_token'


@dataclass(init=False, repr=False, eq=False, frozen=True, match_args=False)
class _UserDataValidation:
    MAX_LEN_PASSWORD: int = 255
    MAX_LEN_LOGIN: int = 32


user_data_validation = _UserDataValidation()
token_types = _TokenType()


API_RESPONSES = {
    'user_account': {
        200: {
            'model': UserInfoResponse,
            'description': 'Информация об аккаунте авторизованного'
                           ' пользователя была успешно возвращена',
        },
        401: {
            'description': 'Токен доступа пользователя не является валидным',
        },
    },
    'change_user_info': {
        200: {
            'description': 'Данные о пользователе были изменены',
        },
        400: {
            'description': 'Недействительный или истекший токен',
        },
    },
    'register': {
        201: {
            'description': 'Пользователь был успешно зарегистрирован',
        },
        400: {
            'description': 'Пользователь ввел данные, которые не соответствуют '
                           'политике API',
        },
    },
    'login': {
        200: {
            'model': JWTResponse,
            'description': 'Пользователь был успешно авторизован',
        },
        400: {
            'description': 'Пользователь ввел некорректные данные',
        },
    },
    'logout': {
        200: {
            'model': JWTResponse,
            'description': 'Токены пользователя были успешно просрочены',
        },
        401: {
            'description': 'Refresh token пользователя не является валидным',
        },
    },
    'tokens': {
        200: {
            'model': JWTResponse,
            'description': 'Access и Refresh токены '
                           'пользователя были успешно обновлены',
        },
        401: {
            'description': 'Refresh token пользователя не является валидным',
        },
    },
    'check_tokens': {
        200: {
            'description': 'Refresh token пользователя является валидным',
        },
        401: {
            'description': 'Refresh token пользователя не является валидным',
        },
    },
    'create_game_session': {
        200: {
            'model': GameSessionResponse,
            'description': 'Сессия успешно создана',
        },
        400: {
            'description': 'Недействительный или истекший токен',
        },
    },
}
