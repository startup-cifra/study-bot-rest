from datetime import datetime
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

import app.models as models
from app.queries.homework import check_deadline_for_group, check_homewroks, create_homework
from app.utils import format_records


homework_router = APIRouter(tags=["Homeworks"])


@homework_router.post('/homeworks', response_model=models.SuccessfulResponse, status_code=status.HTTP_201_CREATED)
async def add_lesson(homework: models.Homework) -> models.SuccessfulResponse:
    await create_homework(homework)
    return models.SuccessfulResponse()


@homework_router.get('/homeworks/deadline', response_model=models.Homework, status_code=status.HTTP_200_OK)
async def check_deadline(date: datetime, chat_id: int) -> models.Homework:
    deadline = await check_deadline_for_group(date, chat_id)
    return models.Homework(deadline=deadline)


# TODO: ВЫБОР выполненые. не выполненные TODO добавить в бд оценку дз
@homework_router.get('/homeworks/user')
async def homeworks_check(tg_id: int) -> JSONResponse:
    homeworks = format_records(await check_homewroks(tg_id))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'homeworks': homeworks,
    })
