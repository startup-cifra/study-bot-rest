import logging
from datetime import datetime, timedelta
from asyncpg import Record
from datetime import datetime
from asyncpg import Record,PostgresError
from app.exceptions import InternalServerError
from app.migrations.db import DB
from app.models import Homework

logger = logging.getLogger(__name__)

async def create_homework(homework: Homework) -> None:
    try:
        sql = """INSERT INTO homework (owner_id , name, deadline, url, chat_id)
                 VALUES($1,$2,$3,$4,$5)
                 RETURNING id """
        hw_id = await DB.fetchval(sql, homework.owner_id, homework.name,
                                  homework.deadline.replace(tzinfo=None), homework.url, homework.chat_id)
        sql = """INSERT INTO users_hw (tg_id, hw_id)
                 SELECT ug.tg_id,
                        $1
                 FROM users_groups ug
                 WHERE ug."role" = 'student'
                    AND ug.chat_id = $2 """
        await DB.execute(sql, hw_id, homework.chat_id)
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError() from error


async def check_deadline_for_group(date: datetime, chat_id: int) -> Record:
    try:
        date = date + timedelta(days=1)
        sql = """SELECT deadline,
                     name,
                     url
                 FROM homework
                 WHERE deadline <= $2
                   AND chat_id = $1 """
        return await DB.fetch(sql, chat_id, date.replace(tzinfo=None))
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError() from error

async def check_homewroks(tg_id: int, cur: bool) -> Record:
    try:
        if cur:
            sql = """SELECT h.name,
                       h.owner_id,
                       h.deadline,
                       h.url,
                       uh.mark
                  FROM homework h
                  JOIN users_hw uh
                  ON h.id = uh.hw_id
                  WHERE uh.tg_id = $1
                    AND uh.mark IS NOT NULL"""
        else:
            sql = """SELECT h.name,
                       h.owner_id,
                       h.deadline,
                       h.url,
                       uh.mark
                  FROM homework h
                  JOIN users_hw uh
                  ON h.id = uh.hw_id
                  WHERE uh.tg_id = $1
                    AND uh.mark IS  NULL"""
        return await DB.fetch(sql, tg_id)
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError() from error
