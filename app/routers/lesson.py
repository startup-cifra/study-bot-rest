from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from app.models import Lessons
from app.queries.lesson import add_lesson_sql, get_les_attedance, lesson_attedance_sql, lessons_for_users
from app.utils import format_records


lessons_router = APIRouter(tags=["Lessons"])


@lessons_router.post('/lessons')
async def add_lesson(lesson: Lessons) -> JSONResponse:
    await add_lesson_sql(lesson)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Executed',
    })


@lessons_router.post('/lessons/attedance')
async def lesson_attedance(date: str = Query(None, description="Дата формата ГГ-ММ-ДД"),
                           owner_id: int = Query(None, description="Id tutor"),
                           attedance: int = Query(None, description="Посещаемость")) -> JSONResponse:

    await lesson_attedance_sql(date, attedance, owner_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Executed',
    })


@lessons_router.get('/lessons/attedance')
async def get_lesson_attedance(date: str = Query(None, description="Дата формата ГГ-ММ-ДД"), 
                               owner_id: int = Query(None, description="Id tutor")) -> JSONResponse:
    attedance = await get_les_attedance(date, owner_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'Attedance': attedance,
    })


# Можно сделать вывод имени преподователя
@lessons_router.get('/lesson')
async def lesson_get_for_users(chat_id: int) -> JSONResponse:
    lessons = format_records(await lessons_for_users(chat_id))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'Lessons': lessons,
    })


@lessons_router.get('/lessons/tutor')
async def lessons_for_tutor(date: str = Query(None, description="Откуда начинать формата ГГ-ММ-ДД"), 
                            owner_id: int = Query(None, description="Id tutor"),
                            chat_id: int = Query(None, description="Группа")) -> JSONResponse:
    lessons = format_records(await lessons_for_tutor(date, owner_id, chat_id))
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'Lessons': lessons,
    })

