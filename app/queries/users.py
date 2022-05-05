from asyncpg import Record
from app.migrations.db import DB
from app.models import UserStudent


async def get_user_groups(tg_id: int) -> list[Record]:
    sql = """SELECT g.name,g.chat_id FROM groups AS g
             JOIN users_groups AS ug
             ON g.chat_id = ug.chat_id
             WHERE ug.tg_id = $1;"""
    return await DB.fetch(sql, tg_id)


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
