import logging

from fastapi import status
from asyncpg.exceptions import PostgresError, UniqueViolationError, ForeignKeyViolationError


logger = logging.getLogger(__name__)


class CommonException(Exception):
    def __init__(self, code: int, error: str) -> None:
        super().__init__()
        self.error = error
        self.code = code


class NotFoundException(CommonException):
    def __init__(self, error: str) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, error)


class UserNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__('Нет такого пользователя')


class InternalServerError(CommonException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Внутренняя ошибка')


class BadRequest(CommonException):
    def __init__(self, error: str) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, error)


class ForbiddenException(CommonException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, "Запрещено")


def db_exception_handler(func):
    def handle_exceptions(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except UniqueViolationError as error:
            logger.error(error)
            return False
        except ForeignKeyViolationError as error:
            logger.error(error)
            return False
        except PostgresError as error:
            logger.error(error)
            raise InternalServerError() from error
        except Exception as error:
            logger.error(error)
    return handle_exceptions
