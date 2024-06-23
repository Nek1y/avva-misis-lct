from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import requests

import src.database.general_db as db
import src.database.models.models as models
from src.services.api.general_api import *
from src.schemas.general_schemas import *
from src.services.gpt import yagpt_answer, generate_by_theme


async def create_report(session: AsyncSession, user_id: int, report_data: ReportCreate):
    report_data = await db.create_report(session, user_id, report_data)
    return report_data


async def save_doc(session: AsyncSession, user_id: int, report_data: ReportCreate):
    if report_data.report_type != ReportType.doc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Need to use report_type = doc, to save generated report'
        )

    doc_data = await create_report(session, user_id, report_data)
    return doc_data


async def get_all_report_by_type(session: AsyncSession, user_id: int, report_type: ReportType):
    report_list = await db.get_all_reports_by_type(session, user_id, report_type)
    return report_list


async def get_report_by_id(session: AsyncSession, user_id: int, report_id: int, report_type: ReportType):
    report_data = await db.get_report_by_id(session, user_id, report_id, report_type)
    return report_data


async def update_report_by_id(session: AsyncSession, user_id: int, report_id: int, report_data: ReportUpdate):
    report_data = await db.update_report(session, user_id, report_id, report_data)
    return report_data


# TODO извлечь данные из шаблона, засунуть в алгоритм поиска инфы и сохранить в поля json_data внутри блоков
async def generate_doc(session: AsyncSession, user_id: int, report_id: int):
    report_data = await get_report_by_id(session, user_id, report_id, ReportType.template)

    # theme = report_data.report_settings.full_theme
    # res = generate_by_theme(theme)

    new_blocks = []
    for block in report_data.blocks:
        new_block = block.model_copy()
        new_block.json_data = await proc_block_params(report_data.report_settings, block, report_data.links)
        new_blocks.append(new_block)

    report_new_data = report_data.model_copy()
    report_new_data.blocks = new_blocks

    result = report_new_data
    return result

# TODO Вот тут передаем данные с блока, получаем итоговый результат
# Плюс надо расписать обрашение к апишке
async def proc_block_params(settings_data: ReportSettingRead, block_data: BlockRead, links: LinkRead | None = None):
    print('Идет запрос к ML')
    json_data = {}
    return json_data

