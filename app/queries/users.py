import logging

from asyncpg import PostgresError, Record

from app.exceptions import InternalServerError
from app.migrations.db import DB
from app.models import UserStudent


logger = logging.getLogger(__name__)


async def add_user_sql(student: UserStudent) -> None:
    sql = """INSERT INTO users(username, tg_id, name, surname, course , faculty)
             VALUES($1,$2,$3,$4,$5,$6)"""
    await DB.fetchval(sql, student.user_name, student.tg_id, student.name_student,
                      student.surname, student.course, student.faculty)


# TODO УБРАТЬ это и вставить проверку в каждую функцию, где надо
async def check_role_sql(tg_id: int, chat_id: int) -> Record:
    sql = """ SELECT role
              FROM users_groups
              WHERE tg_id = $1
                AND chat_id = $2  """
    return await DB.fetchval(sql, tg_id, chat_id)
