from pydantic_settings import BaseSettings


class _AuthConfig(BaseSettings):
    algorithm: str = 'RS256'
    access_token_exp_mins: int = 5
    refresh_token_exp_days: int = 30


auth_config = _AuthConfig()
