from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from fastapi import HTTPException, status

from .models.models import *
import src.schemas.general_schemas as schema
from .db import Base


async def create_object(session: AsyncSession, table_obj: Base, data: list[BaseModel], responce_model: BaseModel | None = None):
    new_obj_list = []

    for sub_data in data:
        new_obj = table_obj(**sub_data.model_dump())
        session.add(new_obj)
        await session.flush()
        new_obj_list.append(new_obj)

    await session.commit()

    if responce_model:
        new_obj_list = [responce_model.model_validate(obj, from_attributes=True) for obj in new_obj_list]

    return new_obj_list


async def get_obj_list(session: AsyncSession, table_obj: Base, responce_model: BaseModel | None = None, id_list: list[int] | None = None):
    expr = select(table_obj)

    if id_list:
        expr = expr.where(table_obj.id.in_(id_list))

    obj_list = await session.execute(expr)
    obj_list = obj_list.scalars().all()

    if responce_model:
        obj_list = [responce_model.model_validate(obj, from_attributes=True) for obj in obj_list]

    return obj_list


async def get_obj_list_by_join(session: AsyncSession, table_obj: Base, join_table_obj: Base, join_id_name: str, condition_id_name: str, condition_id, responce_model: BaseModel | None = None):
    obj_list = await session.execute(
        select(
            table_obj
        ).join(
            join_table_obj,
            join_table_obj.id == table_obj.__get_attr__(join_id_name)
        ).where(
            join_table_obj.__get_attr__(condition_id_name) == condition_id
        )
    )
    obj_list = obj_list.scalars().all()

    if responce_model:
        obj_list = [responce_model.model_validate(obj, from_attributes=True) for obj in obj_list]

    return obj_list


async def get_obj_by_id(session: AsyncSession, table_obj: Base, obj_id: int, responce_model: BaseModel | None = None):
    obj_res = await session.execute(
        select(
            table_obj
        ).where(
            table_obj.id == obj_id
        )
    )
    obj_res = obj_res.scalar_one_or_none()
    if not obj_res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{table_obj.__table__.name}.id = {obj_id} does not exist'
        )

    if responce_model:
        obj_res = responce_model.model_validate(obj_res, from_attributes=True)

    return obj_res


async def update_obj_by_id(session: AsyncSession, table_obj: Base, obj_id: int, data: BaseModel):
    obj_res = await session.execute(
        select(
            table_obj
        ).where(
            table_obj.id == obj_id
        )
    )
    obj_res = obj_res.scalar_one_or_none()

    if not obj_res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{table_obj.__table__.name}.id = {obj_id} does not exist'
        )

    await obj_res.update(**data.model_dump())
    await session.commit()


async def check_id_by_model(session: AsyncSession, table_obj: Base, check_id: int):
    check = await session.execute(
        select(
            table_obj.id
        ).where(
            table_obj.id == check_id
        )
    )
    check = check.scalar_one_or_none()
    if not check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{table_obj.__table__.name}.id = {check_id} does not exist'
        )


async def check_id_set_by_model(session: AsyncSession, table_obj: Base, check_id_set: set[int]):
    model_id_list = await session.execute(
        select(
            table_obj.id
        ).where(
            table_obj.id.in_(check_id_set)
        )
    )
    model_id_list = model_id_list.scalars().all()
    model_id_list = set(model_id_list)

    if model_id_list != check_id_set:
        exclude_product_id = check_id_set - model_id_list

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{table_obj.__table__.name}.id in {exclude_product_id} does not exist'
        )

### SPECIFIC DB PROC
async def get_plant_list(session: AsyncSession, id_list: list[int] | None = None):
    expr = select(Plants, Plants)

    if id_list:
        expr = expr.where(Plants.id.in_(id_list))

    plants_list = await session.execute(expr)
    plants_list = [schema.GeneralPlantGet.model_validate(plant, from_attributes=True) for plant in plants_list]

    return plants_list


async def create_plant(session: AsyncSession, plant_data_list: list[schema.GeneralPlantCreate]):
    new_plant_list = []
    for sub_data in plant_data_list:
        plant = Plants(**sub_data.model_dump())
        session.add(plant)
        await session.flush()
        new_plant_list.append(plant)

    await session.commit()
    new_plant_list = [schema.GeneralPlantGet.model_validate(plant, from_attributes=True) for plant in new_plant_list]

    return new_plant_list


async def get_plant_by_id(session: AsyncSession, plant_id: int):
    plant = await session.execute(
        select(
            Plants
        ).where(
            Plants.id == plant_id
        )
    )
    plant = plant.scalar_one_or_none()
    plant = schema.GeneralPlantGet.model_validate(plant, from_attributes=True)
    return plant


async def update_plant_by_id(session: AsyncSession, plant_id: int, plant_data: schema.GeneralPlantCreate):
    await check_id_by_model(session, Plants, plant_id)

    plant = await session.execute(
        select(
            Plants
        ).where(
            Plants.id == plant_id
        )
    )

    plant = plant.scalar_one_or_none()
    await plant.update(**plant_data.model_dump())
