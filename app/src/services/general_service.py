import random

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.database.general_db as db
import src.database.models.models as models
from src.services.api.general_api import *
from src.schemas.general_schemas import *


async def get_plant_list(session: AsyncSession, id_list: list[int] | None = None):
    plant_list = await db.get_plant_list(session, id_list)
    return plant_list


async def create_plant(session: AsyncSession, user_id: int, plant_data_list: list[GeneralPlantCreate]):
    new_plant = await db.create_plant(session, user_id, plant_data_list)
    return new_plant


async def get_plant_by_id(session: AsyncSession, plant_id: int):
    plant = await db.get_plant_by_id(session, plant_id)
    return plant


async def update_plant_by_id(session: AsyncSession, plant_id: int, plant_data: GeneralPlantCreate):
    await db.update_plant_by_id(session, plant_id, plant_data)
