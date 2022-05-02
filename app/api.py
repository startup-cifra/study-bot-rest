import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import CommonException
from app.migrations.db import DB
from app.routers.groups import groups_router
from app.routers.homework import homework_router
from app.routers.lesson import lessons_router
from app.routers.message import message_router
from app.routers.users import users_router

logger = logging.getLogger(__name__)

app = FastAPI(title='Telegram Bot')


@app.on_event('startup')
async def startup() -> None:
    await DB.connect_db()


@app.on_event('shutdown')
async def shutdown() -> None:
    await DB.disconnect_db()


@app.exception_handler(CommonException)
async def common_exception_handler(request: Request, exception: CommonException):
    return JSONResponse(
        status_code=exception.code,
        content={'details': exception.error}
    )


app.include_router(message_router)
app.include_router(users_router)
app.include_router(lessons_router)
app.include_router(homework_router)
app.include_router(groups_router)
