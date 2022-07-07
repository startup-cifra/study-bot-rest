from fastapi import APIRouter, BackgroundTasks, Query, status

from app import models
from app.queries import homework as homework_queries
from app.queries.users import get_permission_level_for_hw
from app.utils import format_records

homework_router = APIRouter(tags=["Homeworks"])


@homework_router.post('/homeworks', response_model=models.SuccessfulResponse, status_code=status.HTTP_201_CREATED)
async def add_homework(homework: models.Homework, background_tasks: BackgroundTasks) -> models.SuccessfulResponse:
    # !!! background_task завершается после первого вызова await внутри create_homework
    await homework_queries.create_homework(homework)
    # background_tasks.add_task(homework_queries.create_homework, homework)
    return models.SuccessfulResponse()


@homework_router.get('/homeworks/deadline', response_model=list[models.HomeworkOut])
async def check_deadline(date: str = Query(None, title='Дата формата ГГ-ММ-ДД, +1 ОТ ТЕКУЩЕЙ'),
                         chat_id: int = Query(None, title='чат ID')) -> list[models.HomeworkOut]:
    deadline = format_records(await homework_queries.check_deadline_for_group(date, chat_id), models.HomeworkOut)
    return deadline


@homework_router.get('/homeworks/upcomming', response_model=list[models.СheckHomeworkOut])
async def check_upcomming(chat_id: int) -> list[models.СheckHomeworkOut]:
    upcomming = format_records(await homework_queries.check_upcomming_for_group(chat_id), models.СheckHomeworkOut)
    return upcomming


@homework_router.get('/homeworks/user', response_model=list[models.СheckHomeworkOut])
async def homeworks_check(tg_id: int, cur: bool) -> list[models.СheckHomeworkOut]:
    homeworks = format_records(await homework_queries.check_homewroks(tg_id, cur), models.СheckHomeworkOut)
    return homeworks


@homework_router.get('/homeworks/user/owned', response_model=list[models.СheckHomeworkOut])
async def homeworks_owned_check(tg_id: int, chat_id: int) -> list[models.СheckHomeworkOut]:
    homeworks = format_records(await homework_queries.get_all_owned_homeworks_in_chat(tg_id, chat_id),
                               models.СheckHomeworkOut)
    return homeworks


@homework_router.get('/homeworks/group/users', response_model=list[models.UserStudent])
async def get_homeworks_in_group_by_hw_id(chat_id: int, hw_id: int) -> list[models.UserStudent]:
    users = format_records(await homework_queries.get_users_in_group_with_hw(chat_id, hw_id), models.UserStudent)
    return users


@homework_router.put('/homeworks/user/mark', response_model=models.SuccessfulResponse)
async def set_mark_hw(mark: models.HomeworkMark):
    role = await get_permission_level_for_hw(mark.owner_id)
    await homework_queries.set_mark(mark.tg_id, mark.hw_id, mark.mark, role)
    return models.SuccessfulResponse()


@homework_router.get('/homework', response_model=list[models.HomeworkUserOut])
async def get_hw_progress(hw_id: int, owner_id: int) -> list[models.HomeworkUserOut]:
    role = await get_permission_level_for_hw(owner_id)
    homeworks = format_records(await homework_queries.get_hw_people_progress(hw_id, role), models.HomeworkUserOut)
    return homeworks
