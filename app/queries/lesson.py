from datetime import datetime
from app.migrations.db import DB
from app.models import Lessons
from asyncpg import Record


async def add_lesson_sql(lesson: Lessons) -> None:
    sql = """INSERT INTO lesson (owner_id, chat_id, attedance, lesson_type, body, data )
             VALUES($1,$2,0,$3,$4,$5)   """
    await DB.execute(sql, lesson.owner_id, lesson.chat_id, lesson.lesson_type,
                     lesson.body, lesson.date.replace(tzinfo=None))


# получаем айди урока TODO
async def check_lesson(date: datetime, owner_id: int):
    pass


# посещаемость TODO
async def lesson_attedance_sql(date: str, attedance: int, owner_id: int) -> None:
    sql = f"""  UPDATE lesson
                SET attedance = $1
                WHERE CURRENT_DATE = '{date}'
                AND owner_id = $2"""
    await DB.execute(sql, attedance, owner_id)


# может добавить тип урока и группу? :TODO
async def get_les_attedance(date: str, owner_id: int) -> Record:
    sql = f"""  SELECT attedance
                FROM lesson l
                WHERE CURRENT_DATE = '{date}'
                AND owner_id = $1"""
    return await DB.fetchval(sql, owner_id)


async def lessons_for_users(chat_id: int) -> Record:
    sql = """ SELECT lesson_type,
                     body,
                     data
              FROM lesson
              WHERE chat_id = $1"""
    return await DB.fetchrow(sql, chat_id)


async def lessons_for_tutor(date: str, owner_id: int, chat_id: int) -> Record:
    sql = f"""SELECT lesson_type,
                     body,
                     data,
                     attedance
              FROM lesson
              WHERE chat_id = $1
              AND owner_id = $2
              AND CURRENT_DATE >= '{date}'  """
    return await DB.fetchrow(sql, chat_id, owner_id)