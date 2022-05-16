from asyncpg import Record
from app.exceptions import BadRequest
from app.migrations.db import DB
from app.models import UserStudent


async def add_user_sql(student: UserStudent) -> None:
    sql = """INSERT INTO users(username, tg_id, name, surname, course , faculty)
             VALUES($1,$2,$3,$4,$5,$6)"""
    await DB.con.fetchval(sql, student.user_name, student.tg_id, student.name_student,
                          student.surname, student.course, student.faculty)


# TODO может быть надо переработать дял вывода интерфейса в боте(
# Взависимости от роли функционал, если нету предложить вступить в курс какой-нибудь
# по какому признаку или предложить создать курс)
async def check_role_sql(tg_id: int, chat_id: int) -> Record:
    sql = """ SELECT role
              FROM users_groups
              WHERE tg_id = $1
                AND chat_id = $2  """
    role = await DB.con.fetchval(sql, tg_id, chat_id)
    if role is None:
        raise BadRequest(error='Пользователя или группы не существует') from None
    return role
