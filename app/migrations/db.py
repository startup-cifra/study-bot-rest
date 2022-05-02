import logging

import asyncpg
from asyncpg import Record

from app.exceptions import InternalServerError, db_exception_handler
from app.settings import DATABASE_URL

logger = logging.getLogger(__name__)

class DB:
    con: asyncpg.connection.Connection = None

    @classmethod
    @db_exception_handler
    async def connect_db(cls) -> None:
        cls.con = await asyncpg.connect(DATABASE_URL)

    @classmethod
    @db_exception_handler
    async def disconnect_db(cls) -> None:
        await cls.con.close()

    @classmethod
    @db_exception_handler
    async def execute(cls,sql, *args) -> bool:
        return await DB.con.execute(sql,*args)

    @classmethod
    @db_exception_handler
    async def executemany(cls,sql,*args) -> bool:
        return await DB.con.executemany(sql,*args)

    @classmethod
    @db_exception_handler
    async def fetch(cls,sql, *args) -> list[Record]:
        return await DB.con.fetch(sql,*args)

    @classmethod
    @db_exception_handler
    async def fetchrow(cls,sql, *args) -> Record:
        return await DB.con.fetchrow(sql,*args)

    @classmethod
    @db_exception_handler
    async def fetchval(cls,sql, *args):
        return await DB.con.fetchval(sql,*args)
