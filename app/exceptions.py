from fastapi import status


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
    def __init__(self, error: str) -> None:
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, error)


class BadRequest(CommonException):
    def __init__(self, error: str) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, error)


class ForbiddenException(CommonException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, "Forbidden")
