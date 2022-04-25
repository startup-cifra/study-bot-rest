from datetime import datetime
from app.migrations.db import DB
from app.models import Homework
from asyncpg import Record


async def create_homework(homework: Homework) -> None:
    sql = """INSERT INTO homework (owner_id , name, deadline, url)
             VALUES($1,$2,$3,$4) """
    DB.execute(sql, homework.owner_id, homework.name,
               homework.deadline, homework.url)


# TODO пофиксить запрос и почекать
async def check_deadline_for_group(date: datetime, chat_id: int) -> Record:
    sql = f"""SELECT deadline,
                     name,
                     url
                FROM homework
                WHERE CURRENT_DATE <= '{date + 1}'
                AND chat_id = $1 """
    return await DB.fetchrow(sql, chat_id)


async def check_homewroks(tg_id: int) -> Record:
    pass
