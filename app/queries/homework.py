from datetime import datetime, timedelta

from asyncpg import Record

from app.exceptions import ForbiddenException
from app.migrations.db import DB
from app.models import Homework


# TODO: требуются статистические функции по типу, частотная характеристика по домашке, средний балл, топ людей и прочее

async def create_homework(homework: Homework) -> None:
    sql = """INSERT INTO homework (owner_id , name, deadline, url, chat_id)
                 VALUES($1,$2,$3,$4,$5)
                 RETURNING id """
    hw_id = await DB.con.fetchval(sql, homework.owner_id, homework.name,
                                  homework.deadline.replace(tzinfo=None), homework.url, homework.chat_id)
    sql = """INSERT INTO users_hw (tg_id, hw_id)
             SELECT ug.tg_id,
                    $1
             FROM users_groups ug
             WHERE ug.role = 'student'
               AND ug.chat_id = $2 """
    await DB.con.execute(sql, hw_id, homework.chat_id)


async def check_deadline_for_group(date: datetime, chat_id: int) -> Record:
    date = date + timedelta(days=1)
    sql = """SELECT id as hw_id,
                    deadline,
                    name,
                    url
             FROM homework
             WHERE deadline <= $2
               AND chat_id = $1 """
    return await DB.con.fetch(sql, chat_id, date.replace(tzinfo=None))


async def check_upcomming_for_group(chat_id: int) -> Record:
    sql = """SELECT name,
                    url,
                    deadline
             FROM homework 
             WHERE chat_id = $1
               AND deadline >= now()"""
    return await DB.con.fetch(sql, chat_id)


async def get_all_owned_homeworks_in_chat(tg_id: int, chat_id: int):
    sql = """SELECT h.id as hw_id,
                    h.name,
                    h.deadline
             FROM homework h
             WHERE h.owner_id = $1
               AND h.chat_id = $2"""
    return await DB.con.fetch(sql, tg_id, chat_id)


async def check_homewroks(tg_id: int, cur: bool) -> list[Record]:
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
    return await DB.con.fetch(sql, tg_id)


async def set_mark(tg_id: int, hw_id: int, mark: int, role: str) -> None:
    if role != 'tutor':
        raise ForbiddenException()
    sql = """UPDATE users_hw 
             SET mark = $1
             WHERE tg_id = $2
               AND hw_id = $3"""
    await DB.con.execute(sql, mark, tg_id, hw_id)


async def get_users_in_group_with_hw(chat_id: int, hw_id: int) -> list[Record]:
    sql = """SELECT u.tg_id,
                    u.name,
                    u.surname
             FROM users u 
             JOIN users_groups ug 
             ON u.tg_id = ug.tg_id
             JOIN users_hw uh
             ON u.tg_id = uh.tg_id
             WHERE ug.chat_id = $1
               AND uh.hw_id = $2"""
    return await DB.con.fetch(sql, chat_id, hw_id)


async def get_hw_people_progress(hw_id: int, role: str) -> list[Record]:
    if role != 'tutor':
        raise ForbiddenException()
    sql = """SELECT u.name,
                    u.surname,
                    uh.mark
             FROM users u
             JOIN users_hw uh 
             ON u.tg_id = uh.tg_id
             WHERE uh.hw_id = $1"""
    return await DB.con.fetch(sql, hw_id)
