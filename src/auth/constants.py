from dataclasses import dataclass

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
    'logout': {
        200: {
            'model': JWTResponse,
            'description': 'Токены пользователя были успешно просрочены',
        },
        401: {
            'description': 'Refresh token пользователя не является валидным',
        },
    },
}
