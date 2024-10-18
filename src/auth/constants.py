from dataclasses import dataclass

from src.account.schemas import GameSessionResponse, UserInfoResponse
from src.auth.schemas import JWTResponse


@dataclass(init=False, repr=False, eq=False, frozen=True, match_args=False)
class TokenType:
    ACCESS: str = 'access_token'
    REFRESH: str = 'refresh_token'


@dataclass(init=False, repr=False, eq=False, frozen=True, match_args=False)
class _UserDataValidation:
    MAX_LEN_PASSWORD: int = 255
    MAX_LEN_LOGIN: int = 32


@dataclass(init=False, repr=False, eq=False, frozen=True, match_args=False)
class _EmailValidation:
    MAX_LEN_EMAIL: int = 64
    MIN_LEN_EMAIL: int = 6


user_data_validation = _UserDataValidation()
email_validation = _EmailValidation()


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
