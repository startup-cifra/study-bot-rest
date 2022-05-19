from asyncpg import Record

from app.migrations.db import DB


async def add_group(chat_id: int, name: str) -> None:
    sql = """INSERT INTO groups(chat_id, name)
             VALUES ($1, $2)"""
    await DB.con.execute(sql, chat_id, name)


async def add_user_to_group(tg_id: int, chat_id: int, role: str) -> None:
    sql = """INSERT INTO users_groups(tg_id, chat_id, role)
             VALUES ($1, $2, $3)"""
    await DB.con.execute(sql, tg_id, chat_id, role)


async def get_user_groups(tg_id: int) -> list[Record]:
    sql = """SELECT g.name,g.chat_id FROM groups AS g
             JOIN users_groups AS ug
             ON g.chat_id = ug.chat_id
             WHERE ug.tg_id = $1;"""
    return await DB.con.fetch(sql, tg_id)


async def get_users_in_group(chat_id: int) -> list[Record]:
    sql = """SELECT u.tg_id,
                    u.name,
                    u.surname
             FROM users u 
             JOIN users_groups ug 
             ON u.tg_id = ug.tg_id
             WHERE ug.chat_id = $1"""
    return await DB.con.fetch(sql, chat_id)


async def remove_user_from_group(tg_id: int, chat_id: int) -> None:
    sql = """DELETE FROM users_groups
             WHERE tg_id = $1
               AND chat_id = $2"""
    await DB.con.execute(sql, tg_id, chat_id)
