import logging

import asyncpg 
from asyncpg.exceptions import PostgresError, UniqueViolationError, ForeignKeyViolationError
from asyncpg import Record

from app.exceptions import InternalServerError
from app.settings import DATABASE_URL

logger = logging.getLogger(__name__)

class DB:
    con: asyncpg.connection.Connection = None

    @classmethod
    async def connect_db(cls) -> None:
        try:
            cls.con = await asyncpg.connect(DATABASE_URL)
        except Exception as error:
            logger.error(error)

    @classmethod
    async def disconnect_db(cls) -> None:
        await cls.con.close()

    @classmethod
    async def execute(cls,sql, *args) -> bool:
        try:
            await DB.con.execute(sql,*args)
        except UniqueViolationError:
            return False
        except ForeignKeyViolationError:
            return False
        except PostgresError as error:
            raise InternalServerError(str(error)) from error
        return True

    @classmethod
    async def executemany(cls,sql,*args) -> bool:
        try:
            await DB.con.executemany(sql,*args)
        except UniqueViolationError:
            return False
        except ForeignKeyViolationError:
            return False
        except PostgresError as error:
            raise InternalServerError(str(error)) from error
        return True

    @classmethod
    async def fetch(cls,sql, *args) -> list[Record]:
        try:
            return await DB.con.fetch(sql,*args)
        except UniqueViolationError:
            return False
        except ForeignKeyViolationError:
            return False
        except PostgresError as error:
            raise InternalServerError(str(error)) from error

    @classmethod
    async def fetchrow(cls,sql, *args) -> Record:
        try:
            return await DB.con.fetchrow(sql,*args)
        except UniqueViolationError:
            return False
        except ForeignKeyViolationError:
            return False
        except PostgresError as error:
            raise InternalServerError(str(error)) from error

    @classmethod
    async def fetchval(cls,sql, *args):
        try:
            return await DB.con.fetchval(sql,*args)
        except UniqueViolationError:
            return False
        except ForeignKeyViolationError:
            return False
        except PostgresError as error:
            raise InternalServerError(str(error)) from error
