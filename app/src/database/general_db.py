from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, func, or_, select, update
# from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
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


# Report
async def create_report(session: AsyncSession, user_id: int, report_data: schema.ReportCreate):
    new_report = Report(
        name=report_data.name,
        report_type=report_data.report_type,
        create_date=report_data.create_date,
        user_id=user_id
    )

    session.add(new_report)
    await session.flush()

    for block_data in report_data.blocks:
        new_block = Block(report_id=new_report.id, **block_data.model_dump())
        session.add(new_block)

    for link_data in report_data.links:
        new_link = Link(report_id=new_report.id, **link_data.model_dump())
        session.add(new_link)

    new_setting = ReportSetting(report_id=new_report.id, **report_data.report_settings.model_dump())
    session.add(new_setting)
    await session.commit()

    await session.refresh(new_report)
    result = await session.execute(
        select(Report)
        .options(
            selectinload(Report.blocks),
            selectinload(Report.links),
            selectinload(Report.report_settings)
        )
        .filter(Report.id == new_report.id)
    )

    result = result.scalar_one_or_none()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ошибка при создании отчета: {report_data}'
        )

    return schema.ReportRead.model_validate(result, from_attributes=True)


async def get_all_reports_by_type(session: AsyncSession, user_id: int, report_type: schema.ReportType):
    result = await session.execute(
        select(
            Report
        ).options(
            selectinload(Report.blocks),
            selectinload(Report.links),
            selectinload(Report.report_settings)
        ).filter(
            Report.user_id == user_id,
            Report.report_type == report_type
        )
    )
    report_list = result.scalars().all()
    report_list = [schema.ReportRead.model_validate(report, from_attributes=True) for report in report_list]
    return report_list


async def get_report_by_id(session: AsyncSession, user_id: int, report_id: int, report_type: schema.ReportType):
    result = await session.execute(
        select(
            Report
        ).options(
            selectinload(Report.blocks),
            selectinload(Report.links),
            selectinload(Report.report_settings)
        ).filter(
            Report.id == report_id,
            Report.user_id == user_id,
            Report.report_type == report_type
        )
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'report_id = {report_id} by user_id = {user_id} does not exist'
        )

    return schema.ReportRead.model_validate(report, from_attributes=True)


async def update_report(session: AsyncSession, user_id: int, report_id: int, report_data: schema.ReportUpdate):
    result = await session.execute(
        select(
            Report
        ).options(
            selectinload(Report.blocks),
            selectinload(Report.links),
            selectinload(Report.report_settings)
        ).filter(
            Report.id == report_id,
            Report.user_id == user_id
        )
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Отчет с report_id = {report_id} от пользователя с user_id = {user_id} не существует'
        )

    report.name = report_data.name
    report.report_type = report_data.report_type
    report.create_date = report_data.create_date

    if report_data.blocks is not None:
        existing_block_ids = {block.id for block in report.blocks}
        new_block_ids = {block.id for block in report_data.blocks}

        # Удаление блоков, отсутствующих в new_block_ids
        for block in report.blocks:
            if block.id not in new_block_ids:
                await session.delete(block)

        for block_data in report_data.blocks:
            if block_data.id in existing_block_ids:
                block = next((b for b in report.blocks if b.id == block_data.id), None)
                if block:
                    for key, value in block_data.dict().items():
                        setattr(block, key, value)
            else:
                new_block = Block(report_id=report.id, **block_data.dict())
                session.add(new_block)

    if report_data.links is not None:
        existing_link_ids = {link.id for link in report.links}
        new_link_ids = {link.id for link in report_data.links}

        # Удаление ссылок, отсутствующих в new_link_ids
        for link in report.links:
            if link.id not in new_link_ids:
                await session.delete(link)

        for link_data in report_data.links:
            if link_data.id in existing_link_ids:
                link = next((l for l in report.links if l.id == link_data.id), None)
                if link:
                    for key, value in link_data.dict().items():
                        setattr(link, key, value)
            else:
                new_link = Link(report_id=report.id, **link_data.dict())
                session.add(new_link)

    if report.report_settings:
        for key, value in report_data.report_settings.dict().items():
            setattr(report.report_settings, key, value)
    else:
        new_setting = ReportSetting(report_id=report.id, **report_data.report_settings.dict())
        session.add(new_setting)

    await session.commit()

    return schema.ReportRead.model_validate(report, from_attributes=True)
