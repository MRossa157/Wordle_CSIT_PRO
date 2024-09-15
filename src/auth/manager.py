from fastapi import Depends
from fastapi_users import BaseUserManager

from src.auth.models import User
from src.auth.utils import get_user_db


class UserManager(BaseUserManager[User, int]):
    user_db_model = User

    async def get_by_username(self, username: str):
        query = await self.user_db_model.query.where(User.username == username)
        return await query.first()

    async def on_after_register(self, user: User, request=None) -> None:
        print(f'User {user.username} has registered.')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
