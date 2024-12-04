from os import getenv
from typing import List

from pydantic_settings import BaseSettings


class _CORSSettings(BaseSettings):
    origins: List[str] = getenv('CORS_ORIGINS').split('|')
    credentials: bool = True
    methods: List[str] = ['*']
    headers: List[str] = ['*']


cors_settings = _CORSSettings()
