from app.migrations.db import DB
from app.models import UserStudent
from asyncpg import Record


async def add_admin_sql(name: str) -> None:
    sql = """UPDATE users 
             SET role = 'tutor'
             WHERE username = '$1' """
    await DB.execute(sql, name)


async def add_user_sql(student: UserStudent) -> None:
    sql = """INSERT INTO users(username, tg_id, role, name, surname, course , faculty)
            VALUES($1,$2,'student',$3,$4,$5,$6)"""
    await DB.fetchval(sql, student.user_name, student.tg_id, student.name_student,
                      student.surname, student.course, student.faculty)


async def check_role_sql(name: str) -> Record:
    sql = """   SELECT role
                FROM users
                WHERE username = $1  """
    return await DB.fetchval(sql, name)
