from asyncpg import Record
from app.migrations.db import DB


async def add_admin_sql(name:str)->None:
    pass

async def get_user_groups(tg_id:int) -> list[Record]:
    sql = """SELECT g.name,g.chat_id FROM groups AS g JOIN users_groups AS ug ON g.chat_id = ug.chat_id WHERE ug.tg_id = $1;"""
    return await DB.fetch(sql,tg_id)
