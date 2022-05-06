import logging
from datetime import datetime
from asyncpg import Record,PostgresError
from app.exceptions import InternalServerError
from app.migrations.db import DB
from app.models import Lessons

logger = logging.getLogger(__name__)

async def add_lesson_sql(lesson: Lessons) -> None:
    sql = """INSERT INTO lesson (owner_id, chat_id, attedance, lesson_type, body, data )
             VALUES($1,$2,0,$3,$4,$5)
             RETURNING id   """
    ls_id = await DB.fetchval(sql, lesson.owner_id, lesson.chat_id, lesson.lesson_type,
                              lesson.body, lesson.date.replace(tzinfo=None))
    sql = """INSERT INTO users_lesson (tg_id, lesson_id)
             SELECT ug.tg_id,
                    $1
             FROM users_groups ug
             WHERE ug."role" = 'student'
                AND ug.chat_id = $2"""
    await DB.execute(sql, ls_id, lesson.chat_id)


# посещаемость TODO
async def lesson_attedance_sql(date: datetime, attedance: int, owner_id: int) -> None:
    sql = """UPDATE lesson
             SET attedance = $1
             WHERE data::date = $3
               AND owner_id = $2"""
    await DB.execute(sql, attedance, owner_id, date)


# может добавить тип урока и группу? :TODO удалить
async def get_les_attedance(date: datetime, owner_id: int) -> Record:
    sql = """SELECT attedance
             FROM lesson l
             WHERE data::date = $2
               AND owner_id = $1"""
    return await DB.fetchval(sql, owner_id, date)


async def lessons_for_users(chat_id: int, date: datetime) -> Record:
    sql = """SELECT lesson_type,
                    body,
                    data,
                    owner_id
             FROM lesson
             WHERE chat_id = $1
               AND data >= $2"""
    return await DB.fetch(sql, chat_id, date.replace(tzinfo=None))


async def lessons_for_tutor_sql(date_start: datetime, date_end: datetime,
                                owner_id: int, chat_id: int) -> Record:
    sql = """SELECT lesson_type,
                     body,
                     data,
                     attedance
              FROM lesson
              WHERE chat_id = $1
              AND owner_id = $2
              AND data >= $3
              AND data <= $4 """
    return await DB.fetch(sql, chat_id, owner_id, date_start.replace(tzinfo=None), date_end.replace(tzinfo=None))
