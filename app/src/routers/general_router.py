from typing import Annotated

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_schemas import *
from src.services.general_service import *
from src.services.auth_utils import get_current_user
from src.database.db import get_session

general_router = APIRouter(
    tags=['General'],
    prefix='/general'
)

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[UserOut, Depends(get_current_user)]
IDList = Annotated[list[int], Query()]


@general_router.get('/test')
async def route_get_plant_list():
    return {'message': 'Тест пройден успешно!'}


# PLANTS
@general_router.get('/plant', response_model=list[GeneralPlantGet])
async def route_get_plant_list(current_user: CurrentUser, session: Session, id_list: IDList = None):
    plant_list = await get_plant_list(session, id_list)
    return plant_list


@general_router.post('/plant', response_model=list[GeneralPlantGet])
async def route_create_plant(plant_data_list: list[GeneralPlantCreate], current_user: CurrentUser, session: Session):
    new_plant = await create_plant(session, plant_data_list)
    return new_plant


@general_router.get('/plant/{plant_id}', response_model=GeneralPlantGet)
async def route_get_plant_by_id(plant_id: int, current_user: CurrentUser, session: Session):
    plant = await get_plant_by_id(session, plant_id)
    return plant


@general_router.patch('/plant/{plant_id}')
async def route_update_plant_by_id(plant_id: int, plant_data: GeneralPlantCreate, current_user: CurrentUser, session: Session):
    await update_plant_by_id(session, plant_id, plant_data)
    data = {
        'message': 'successful'
    }
    return data
