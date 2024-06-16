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
async def route_test_healthcheck():
    return {'message': 'Тест пройден успешно!'}


# REPORT
@general_router.post('/report', response_model=ReportRead)
async def route_create_report(report_data: ReportCreate, current_user: CurrentUser, session: Session):
    report_data = await create_report(session, current_user.id, report_data)
    return report_data


@general_router.get('/report', response_model=list[ReportRead])
async def route_get_all_report(current_user: CurrentUser, session: Session):
    report_list = await get_all_report_by_type(session, current_user.id, report_type=ReportType.template)
    return report_list


@general_router.get('/report/{report_id}', response_model=ReportRead)
async def route_get_report_by_id(report_id: int, current_user: CurrentUser, session: Session):
    report_data = await get_report_by_id(session, current_user.id, report_id, report_type=ReportType.template)
    return report_data


@general_router.patch('/report/{report_id}', response_model=ReportRead)
async def route_update_report_by_id(report_id: int, report_data: ReportUpdate, current_user: CurrentUser, session: Session):
    report_data = await update_report_by_id(session, current_user.id, report_id, report_data)
    return report_data


@general_router.get('/report/{report_id}/generate', response_model=ReportRead)
async def route_generate_doc(report_id: int, current_user: CurrentUser, session: Session):
    report_data = await generate_doc(session, current_user.id, report_id)
    return report_data


# DOC
@general_router.get('/doc', response_model=list[ReportRead])
async def route_get_all_doc(current_user: CurrentUser, session: Session):
    report_list = await get_all_report_by_type(session, current_user.id, report_type=ReportType.doc)
    return report_list


@general_router.get('/doc/{doc_id}', response_model=ReportRead)
async def route_get_doc_by_id(doc_id: int, current_user: CurrentUser, session: Session):
    report_data = await get_report_by_id(session, current_user.id, doc_id, report_type=ReportType.doc)
    return report_data

