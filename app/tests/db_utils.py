from app.migrations.db import DB

async def setup_db():
    await DB.connect_db()
    sql = """INSERT INTO users(tg_id,role,username,name,surname,course,faculty) VALUES ($1,$2,$3,$4,$5,$6,$7)"""
    await DB.execute(sql,123,0,"user1","name1","surname1",1,"faculty1")
    await DB.execute(sql,124,0,"user2","name2","surname2",1,"faculty2")
    await DB.execute(sql,125,0,"user3","name3","surname3",1,"faculty3")
    sql = """INSERT INTO groups(chat_id,name) VALUES ($1,$2)"""
    await DB.execute(sql,)

async def cleanup_db():

    await DB.disconnect_db()
