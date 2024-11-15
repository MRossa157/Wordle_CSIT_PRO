from contextlib import asynccontextmanager
from os import environ

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.account.views import router as account_router
from src.auth.views import router as auth_router
from src.leaderboard.views import router as leaderboard_router
from src.security import cors_settings
from src.utils.database import db_manager
from src.utils.rsa_keys_manager import keys_manager
from src.wordle.crud import remove_not_used_game_sessions
from src.wordle.views import router as wordle_router


@asynccontextmanager
async def _lifespan(app_: FastAPI):  # noqa: ANN202, ARG001
    keys_manager.generate_keys()
    async with db_manager.lifespan():
        scheduler.start()
        yield


app = FastAPI(
    lifespan=_lifespan,
    title='Worlde backend',
)

app.include_router(
    auth_router,
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    account_router,
    prefix='/account',
    tags=['account'],
)

app.include_router(
    wordle_router,
    prefix='/wordle',
    tags=['wordle'],
)

app.include_router(
    leaderboard_router,
    prefix='/leaderboard',
    tags=['leaderboard'],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_settings.origins,
    allow_credentials=cors_settings.credentials,
    allow_methods=cors_settings.methods,
    allow_headers=cors_settings.headers,
)

environ['TZ'] = 'Europe/Saratov'


scheduler = AsyncIOScheduler()
scheduler.add_job(remove_not_used_game_sessions, 'interval', hours=1)
