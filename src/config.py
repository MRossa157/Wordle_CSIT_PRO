from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class DBSettings(AppBaseSettings):
    DATABASE_HOST: str = Field(..., env='DATABASE_HOST')
    DATABASE_PORT: str = Field(..., env='DATABASE_PORT')
    DATABASE_NAME: str = Field(..., env='DATABASE_NAME')
    DATABASE_USER: str = Field(..., env='DATABASE_USER')
    DATABASE_PASSWORD: str = Field(..., env='DATABASE_PASSWORD')


class AppSettings(AppBaseSettings):
    BACK_HOST: str = Field(..., env='BACK_HOST')
    BACK_PORT: int = Field(..., env='BACK_PORT')


class JWTSecret(AppBaseSettings):
    JWT_SECRET: str = Field(..., env='JWT_SECRET')


class PasswordSecret(AppBaseSettings):
    PASSWORD_SECRET: str = Field(..., env='PASSWORD_SECRET')
