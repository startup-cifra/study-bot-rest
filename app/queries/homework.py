from datetime import datetime
from asyncpg import Record
from app.migrations.db import DB
from app.models import Homework


async def create_homework(homework: Homework) -> None:
    sql = """INSERT INTO homework (owner_id , name, deadline, url)
             VALUES($1,$2,$3,$4) """
    await DB.execute(sql, homework.owner_id, homework.name,
                     homework.deadline, homework.url)


# TODO пофиксить запрос и почекать
async def check_deadline_for_group(date: datetime, chat_id: int) -> Record:
    sql = f"""SELECT deadline,
                     name,
                     url
                FROM homework
                WHERE CURRENT_DATE <= '{date + 1}'
                AND owner_id = $1 """
    return await DB.fetchrow(sql, chat_id)


async def check_homewroks(tg_id: int, cur: int) -> Record:
    check_h = 'Null'
    if cur:
        check_h = 'Not' + ' ' + check_h
    sql = f"""select  h.name, 
		      h.owner_id,
		        h.deadline ,
		        h.url,
		        uh.mark
            from homework h 
	        left outer join users_hw uh on h.id = uh.hw_id  where uh.mark IS {check_h} and uh.tg_id =$1 """
    return await DB.fetchrow(sql, tg_id)
    
