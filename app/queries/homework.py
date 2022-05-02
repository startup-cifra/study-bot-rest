import logging
from datetime import datetime
from asyncpg import Record,PostgresError
from app.exceptions import InternalServerError
from app.migrations.db import DB
from app.models import Homework

logger = logging.getLogger(__name__)

async def create_homework(homework: Homework) -> None:
    sql = """INSERT INTO homework (owner_id , name, deadline, url)
             VALUES($1,$2,$3,$4) """
    try:
        await DB.con.execute(sql, homework.owner_id, homework.name,
               homework.deadline, homework.url)
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError() from error

# TODO пофиксить запрос и почекать
async def check_deadline_for_group(date: datetime, chat_id: int) -> Record:
    sql = f"""SELECT deadline,
                     name,
                     url
                FROM homework
                WHERE CURRENT_DATE <= '{date + 1}'
                AND owner_id = $1 """
    try:
        return await DB.con.fetchrow(sql, chat_id)
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError() from error

async def check_homewroks(tg_id: int) -> Record:
    pass
