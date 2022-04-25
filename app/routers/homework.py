from datetime import datetime
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.models import Homework
from app.queries.homework import check_deadline_for_group, check_homewroks, create_homework
from app.utils import format_records


homework_router = APIRouter(tags=["Homeworks"])


@homework_router.post('/homeworks')
async def add_lesson(homework: Homework) -> JSONResponse:
    await create_homework(homework)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Executed',
    })


@homework_router.get('/homeworks/deadline')
async def check_deadline(date: datetime, chat_id: int) -> JSONResponse:
    deadline = format_records(await check_deadline_for_group(date, chat_id))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'deadline': deadline,
    })


# TODO: ВЫБОР выполненые. не выполненные TODO добавить в бд оценку дз
@homework_router.get('/homeworks/user')
async def homeworks_check(tg_id: int) -> JSONResponse:
    homeworks = format_records(await check_homewroks(tg_id))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'homeworks': homeworks,
    })
