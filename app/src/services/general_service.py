from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import requests
import json

import src.database.general_db as db
import src.database.models.models as models
from src.services.api.general_api import *
from src.schemas.general_schemas import *
from src.services.gpt import yagpt_answer, generate_by_theme
from src.services.final_ML.classes import YaGPT


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


async def proc_block_params(settings_data: ReportSettingRead, block_data: BlockRead, links: LinkRead | None = None):
    folder_id = 'b1gvmt1gifb7ug7h620q'
    api_key_search_api = 'AQVN2qWGvXFbx_lvCbG8mc5-olMsTq5xC-53To-N'
    search_api_url = f"https://ya.ru/search/xml/generative?folderid={folder_id}"
    api_key_yagpt = 'AQVNwlwccMNXWq6ugih7-fjIKGtH3tTtf2zmAL2b'

    headers = {"Authorization": f"Api-Key {api_key_search_api}"}
    headers_yagpt = {"Authorization": f"Api-Key {api_key_yagpt}"}

    llm_model = settings_data.llm_model
    search_theme = settings_data.full_theme
    user_theme = settings_data.theme
    links = links
    block_type = block_data.block_type
    axis_x = block_data.axis_x
    axis_y = block_data.axis_y

    ya = YaGPT(
        headers_yagpt=headers_yagpt,
        theme=user_theme,
        full_theme=search_theme,
        links=links,
        block_type=block_type,
        axis_x=axis_x,
        axis_y=axis_y
    )

    new_json_data = ya.search_api(search_api_url, headers)
    return new_json_data
