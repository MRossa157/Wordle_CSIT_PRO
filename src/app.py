import fastapi_users
from fastapi import FastAPI

from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.router import router as auth_router

app = FastAPI(title='Worlde backend')


@app.get('/ping')
async def pong():
    return {'ping': 'pong!'}


fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth',
    tags=['auth'],
)

app.include_router(
    auth_router,
    prefix='/auth',
    tags=['auth'],
)
