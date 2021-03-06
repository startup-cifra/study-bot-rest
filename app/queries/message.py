
from datetime import datetime
from asyncpg import Record
from app.migrations.db import DB
from app.exceptions import BadRequest


# TODO: добавить пагинацию


async def add_new_message(tg_id: int,
                          chat_id: int,
                          body: str,
                          date: datetime) -> None:
    sql = """SELECT tg_id FROM users_groups
             WHERE tg_id = $1 AND chat_id = $2"""
    res = await DB.con.fetch(sql, tg_id, chat_id)
    if not res:
        raise BadRequest('Пользователь не принадлежит группе')
    sql = """INSERT INTO message(tg_id,chat_id,body,date)
             VALUES ($1,$2,$3,$4);"""
    await DB.con.execute(sql, tg_id, chat_id, body, date.replace(tzinfo=None))


async def get_group_messages(chat_id: int,
                             start_date: datetime,
                             end_date: datetime) -> list[Record]:
    sql = """SELECT tg_id,body,date
             FROM message
             WHERE chat_id = $1
               AND date >= $2
               AND date <= $3"""
    return await DB.con.fetch(sql, chat_id, start_date.replace(tzinfo=None), end_date.replace(tzinfo=None))


async def get_group_messages_by_user(tg_id: int,
                                     chat_id: int,
                                     start_date: datetime,
                                     end_date: datetime) -> list[Record]:
    sql = """SELECT body,date
             FROM message
             WHERE tg_id = $1
               AND chat_id = $2
               AND date >= $3
               AND date <= $4"""
    return await DB.con.fetch(sql, tg_id, chat_id, start_date.replace(tzinfo=None), end_date.replace(tzinfo=None))


async def count_group_messages(chat_id: int,
                               start_date: datetime,
                               end_date: datetime) -> int:
    sql = """SELECT COUNT(tg_id)
             FROM message
             WHERE chat_id = $1
               AND date >= $2
               AND date <= $3"""
    return await DB.con.fetchval(sql, chat_id, start_date.replace(tzinfo=None), end_date.replace(tzinfo=None))


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
    count = await DB.con.fetchval(sql, tg_id, chat_id, start_date.replace(tzinfo=None),
                                  end_date.replace(tzinfo=None))
    return count
