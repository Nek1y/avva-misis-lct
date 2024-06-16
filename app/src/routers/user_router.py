from fastapi import APIRouter, Depends

from src.schemas.user_schemas import *
from src.services.user_service import *
from src.services.auth_utils import get_current_user

user_router = APIRouter(
    tags=['User'],
    prefix='/users'
)


@user_router.get('/me', response_model=UserOut)
async def route_get_user(current_user: UserOut = Depends(get_current_user)):
    return current_user


@user_router.patch('/me')
async def route_update_user(new_user_data: UserUpdate, user: UserOut = Depends(get_current_user)):
    await update_user_info(user.id, new_user_data)
    data = {
        'message': 'successful'
    }
    return data
