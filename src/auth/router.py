from fastapi import APIRouter, Depends, HTTPException

from src.auth.manager import UserManager, get_user_manager
from src.auth.schemas import UserCreate

router = APIRouter()


@router.post('/register')
async def register(
    user: UserCreate,
    user_manager: UserManager = Depends(get_user_manager),
):
    existing_user = await user_manager.get_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already taken')
    new_user = await user_manager.create(user)
    return {'msg': 'User registered successfully'}
