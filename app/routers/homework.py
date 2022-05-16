from fastapi import APIRouter, BackgroundTasks, Query, status

from app import models
from app.queries.homework import check_deadline_for_group, check_homewroks, create_homework, set_mark
from app.queries.users import get_permission_level_for_hw
from app.utils import format_records

homework_router = APIRouter(tags=["Homeworks"])


@homework_router.post('/homeworks', response_model=models.SuccessfulResponse, status_code=status.HTTP_201_CREATED)
async def add_homework(homework: models.Homework, background_tasks: BackgroundTasks) -> models.SuccessfulResponse:
    background_tasks.add_task(create_homework, homework)
    return models.SuccessfulResponse()


@homework_router.get('/homeworks/deadline', response_model=list[models.HomeworkOut])
async def check_deadline(date: str = Query(None, title='Дата формата ГГ-ММ-ДД, +1 ОТ ТЕКУЩЕЙ'),
                         chat_id: int = Query(None, title='чат ID')) -> list[models.HomeworkOut]:
    deadline = format_records(await check_deadline_for_group(date, chat_id), models.HomeworkOut)
    return deadline


@homework_router.get('/homeworks/user', response_model=list[models.СheckHomeworkOut])
async def homeworks_check(tg_id: int, cur: bool) -> list[models.СheckHomeworkOut]:
    homeworks = format_records(await check_homewroks(tg_id, cur), models.СheckHomeworkOut)
    return homeworks


@homework_router.put('/homeworks/user/mark', response_model=models.SuccessfulResponse)
async def set_mark_hw(mark: models.HomeworkMark):
    role = await get_permission_level_for_hw(mark.tg_id, mark.hw_id)
    await set_mark(mark.tg_id, mark.hw_id, mark.mark, role)
    return models.SuccessfulResponse()
