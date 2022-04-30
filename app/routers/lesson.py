from fastapi import APIRouter, Query, status
from app import models
from app.queries.lesson import add_lesson_sql, get_les_attedance, lesson_attedance_sql, lessons_for_users
from app.utils import format_records


lessons_router = APIRouter(tags=["Lessons"])


@lessons_router.post('/lessons', response_model=models.SuccessfulResponse, status_code=status.HTTP_200_OK)
async def add_lesson(lesson: models.Lessons) -> models.SuccessfulResponse:
    await add_lesson_sql(lesson)
    return models.SuccessfulResponse()


@lessons_router.post('/lessons/attedance', response_model=models.SuccessfulResponse, status_code=status.HTTP_200_OK)
async def lesson_attedance(date: str = Query(None, description="Дата формата ГГ-ММ-ДД"),
                           owner_id: int = Query(None, description="Id tutor"),
                           attedance: int = Query(None, description="Посещаемость")) -> models.SuccessfulResponse:

    await lesson_attedance_sql(date, attedance, owner_id)
    return models.SuccessfulResponse()


@lessons_router.get('/lessons/attedance', response_model=models.AttendanceOut, status_code=status.HTTP_200_OK)
async def get_lesson_attedance(date: str = Query(None, description="Дата формата ГГ-ММ-ДД"),
                               owner_id: int = Query(None, description="Id tutor")) -> models.AttendanceOut:
    attedance = await get_les_attedance(date, owner_id)
    return models.AttendanceOut(attedance=attedance)


# Можно сделать вывод имени преподователя
@lessons_router.get('/lesson', response_model=list[models.LessonsOut], status_code=status.HTTP_200_OK)
async def lesson_get_for_users(chat_id: int) -> list[models.LessonsOut]:
    lessons = format_records(await lessons_for_users(chat_id),models.LessonsOut)
    return lessons


@lessons_router.get('/lessons/tutor', response_model=list[models.LessonsOut], status_code=status.HTTP_200_OK)
async def lessons_for_tutor(date: str = Query(None, description="Откуда начинать формата ГГ-ММ-ДД"),
                            owner_id: int = Query(None, description="Id tutor"),
                            chat_id: int = Query(None, description="Группа")) -> list[models.LessonsOut]:
    lessons = format_records(await lessons_for_tutor(date, owner_id, chat_id), models.LessonsOut)
    return lessons
