import logging
from datetime import datetime
from asyncpg import PostgresError, ForeignKeyViolationError
from asyncpg import Record
from app.migrations.db import DB
from app.exceptions import BadRequest, NotFoundException, InternalServerError

logger = logging.getLogger(__name__)

# TODO: добавить пагинацию


async def add_new_message(tg_id: int,
                          chat_id: int,
                          body: str,
                          date: datetime) -> None:
    sql = """SELECT tg_id FROM users_groups
             WHERE tg_id = $1 AND chat_id = $2"""
    try:
        res = await DB.con.fetch(sql, tg_id, chat_id)
        if not res:
            raise BadRequest('Пользователь не принадлежит группе')
    except PostgresError as error:
        raise InternalServerError() from error
    sql = """INSERT INTO message(tg_id,chat_id,body,date)
             VALUES ($1,$2,$3,$4);"""
    try:
        await DB.con.execute(sql, tg_id, chat_id, body, date.replace(tzinfo=None))
    except ForeignKeyViolationError as error:
        raise NotFoundException('Пользователь или группа не существует') from error
    except PostgresError as error:
        raise InternalServerError() from error


async def get_group_messages(chat_id: int,
                             start_date: datetime,
                             end_date: datetime) -> list[Record]:
    sql = """SELECT tg_id,body,date
                 FROM message
                 WHERE chat_id = $1 AND date >= $2
                   AND date <= $3"""
    try:
        return await DB.con.fetch(sql, chat_id, start_date.replace(tzinfo=None), end_date.replace(tzinfo=None))
    except PostgresError as error:
        raise InternalServerError() from error


async def get_group_messages_by_user(tg_id: int,
                                     chat_id: int,
                                     start_date: datetime,
                                     end_date: datetime) -> list[Record]:
    sql = """SELECT body,date
                 FROM message
                 WHERE tg_id = $1
                   AND chat_id = $2 AND date >= $3
                   AND date <= $4"""
    try:
        return await DB.con.fetch(sql, tg_id, chat_id, start_date.replace(tzinfo=None), end_date.replace(tzinfo=None))
    except PostgresError as error:
        raise InternalServerError() from error


async def count_group_messages(chat_id: int,
                               start_date: datetime,
                               end_date: datetime) -> int:
    sql = """SELECT COUNT(tg_id)
                 FROM message
                 WHERE chat_id = $1
                   AND date >= $2
                   AND date <= $3"""
    try:
        return await DB.con.fetchval(sql, chat_id, start_date.replace(tzinfo=None), end_date.replace(tzinfo=None))
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError() from error


async def count_group_messages_by_user(tg_id: int,
                                       chat_id: int,
                                       start_date: datetime,
                                       end_date: datetime) -> int:
    sql = """SELECT COUNT(tg_id)
                 FROM message
                 WHERE tg_id = $1
                   AND chat_id = $2
                   AND date >= $3
                   AND date <= $4"""
    try:
        return await DB.con.fetchval(sql, tg_id, chat_id, start_date.replace(tzinfo=None),
                                     end_date.replace(tzinfo=None))
    except PostgresError as error:
        raise InternalServerError() from error
