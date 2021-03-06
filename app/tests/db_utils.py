from datetime import datetime, timedelta

from app.migrations.db import DB


async def setup_db():
    await DB.connect_db()
    await cleanup_db()
    print(DB.con)
    sql = """INSERT INTO users(tg_id,username,name,surname,course,faculty) VALUES ($1,$2,$3,$4,$5,$6)"""
    await DB.con.execute(sql, 123, "user1", "name1", "surname1", 1, "faculty1")
    await DB.con.execute(sql, 124, "user2", "name2", "surname2", 1, "faculty2")
    await DB.con.execute(sql, 125, "user3", "name3", "surname3", 1, "faculty3")
    sql = """INSERT INTO groups(chat_id,name) VALUES ($1,$2)"""
    await DB.con.execute(sql, 123, 'group1')
    await DB.con.execute(sql, 124, 'group2')
    sql = """INSERT INTO users_groups(tg_id,chat_id) VALUES($1,$2)"""
    await DB.con.execute(sql, 123, 123)
    await DB.con.execute(sql, 124, 124)
    await DB.con.execute(sql, 125, 123)
    sql = """INSERT INTO message(tg_id,chat_id,body,date) VALUES($1,$2,$3,$4)"""
    await DB.con.execute(sql, 123, 123, "message1", datetime.now())
    await DB.con.execute(sql, 123, 123, "message2", datetime.now() - timedelta(days=1))
    await DB.con.execute(sql,125,123,"message3",datetime.now())
    await DB.con.execute(sql,124,124,"message4",datetime.now())

async def cleanup_db():
    sql = """DELETE FROM message CASCADE"""
    await DB.con.execute(sql)
    sql = """DELETE FROM users_groups"""
    await DB.con.execute(sql)
    sql = """DELETE FROM groups"""
    await DB.con.execute(sql)
    sql = """DELETE FROM users"""
    await DB.con.execute(sql)

async def close_connection():
    await DB.disconnect_db()
