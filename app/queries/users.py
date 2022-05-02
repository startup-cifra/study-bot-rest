import logging
from asyncpg import Record,PostgresError
from app.exceptions import InternalServerError
from app.migrations.db import DB
from app.models import UserStudent

logger = logging.getLogger(__name__)


async def get_user_groups(tg_id:int) -> list[Record]:
    sql = """SELECT g.name,g.chat_id FROM groups AS g
             JOIN users_groups AS ug 
             ON g.chat_id = ug.chat_id 
             WHERE ug.tg_id = $1;"""
    try:
        return await DB.con.fetch(sql,tg_id)
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError() from error
async def add_admin_sql(name: str) -> None:
    sql = """UPDATE users
             SET role = 'tutor'
             WHERE username = $1 """
    try:
        await DB.con.execute(sql, name)
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError() from error

async def add_user_sql(student: UserStudent) -> None:
    sql = """INSERT INTO users(username, tg_id, role, name, surname, course , faculty)
             VALUES($1,$2,'student',$3,$4,$5,$6)"""
    try:
        await DB.con.fetchval(sql, student.user_name, student.tg_id, student.name_student,
                      student.surname, student.course, student.faculty)
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError() from error

async def check_role_sql(name: str) -> Record:
    sql = """   SELECT role
                FROM users
                WHERE username = $1  """
    try:
        return await DB.con.fetchval(sql, name)
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError() from error