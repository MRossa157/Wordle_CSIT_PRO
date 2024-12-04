from os import getenv

from pydantic_settings import BaseSettings


class _AuthConfig(BaseSettings):
    algorithm: str = 'RS256'
    access_token_exp_mins: int = 30
    long_refresh_token_exp_days: int = 30
    short_refresh_token_exp_days: int = 1


class _CookieConfig(BaseSettings):
    secure: bool = False
    samesite: str = "lax"

    def __init__(self) -> None:
        super().__init__()

        if getenv('DEV_MODE'):
            self.secure = True
            self.samesite = "none"


auth_config = _AuthConfig()
cookie_config = _CookieConfig()
