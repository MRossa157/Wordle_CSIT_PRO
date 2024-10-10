from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.views import router as auth_router
from src.utils.database import db_manager
from src.utils.rsa_keys_manager import keys_manager


@asynccontextmanager
async def _lifespan(app_: FastAPI):
    keys_manager.generate_keys()
    async with db_manager.lifespan():
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
