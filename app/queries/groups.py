import logging

from asyncpg import ForeignKeyViolationError, PostgresError, Record, UniqueViolationError

from app.exceptions import BadRequest, InternalServerError, NotFoundException
from app.migrations.db import DB

logger = logging.getLogger(__name__)


async def add_group(chat_id: int, name: str) -> None:
    sql = """INSERT INTO groups(chat_id, name) VALUES ($1, $2)"""
    try:
        await DB.con.execute(sql, chat_id, name)
    except UniqueViolationError as error:
        logger.error(error)
        raise BadRequest('Группа уже существует') from error
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError from error


async def add_user_to_group(tg_id: int, chat_id: int, role: str) -> None:
    sql = """INSERT INTO users_groups(tg_id, chat_id, role) VALUES ($1, $2, $3)"""
    try:
        await DB.con.execute(sql, tg_id, chat_id, role)
    except UniqueViolationError as error:
        logger.error(error)
        raise BadRequest('Пользователь уже состоит в группе') from error
    except ForeignKeyViolationError as error:
        logger.error(error)
        raise NotFoundException('Группы не существует') from error
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError from error


async def get_user_groups(tg_id: int) -> list[Record]:
    sql = """SELECT g.name,g.chat_id FROM groups AS g
             JOIN users_groups AS ug 
             ON g.chat_id = ug.chat_id 
             WHERE ug.tg_id = $1;"""
    try:
        return await DB.con.fetch(sql, tg_id)
    except PostgresError as error:
        logger.error(error)
        raise InternalServerError() from error
