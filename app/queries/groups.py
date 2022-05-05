
from app.migrations.db import DB


async def create_group(chat_id: int, name: str) -> None:
    sql = """INSERT INTO groups (chat_id, name)
             VALUES($1,$2)"""
    await DB.fetchval(sql, chat_id, name)


async def add_user_group(tg_id: int, chat_id: int) -> None:
    sql = """INSERT INTO users_groups (tg_id, chat_id, role)
             VALUES($1,$2,'student')"""
    await DB.fetchval(sql, tg_id, chat_id)


async def add_admin_in_group(tg_id, chat_id) -> None:
    sql = """ UPDATE users_groups
              SET role =  'tutor'
              Where tg_id = $1
               AND chat_id = $2 """
    await DB.execute(sql, tg_id, chat_id)
