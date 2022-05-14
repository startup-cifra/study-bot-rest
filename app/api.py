
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from app.migrations.db import DB
from app.routers.message import message_router
from app.routers.users import users_router
from app.routers.lesson import lessons_router
from app.routers.homework import homework_router
from app.routers.groups import groups_router
import time
import logging

from logging import getLogger

logger = getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

app = FastAPI(title='Telegram Bot')


@app.on_event('startup')
async def startup() -> None:
    await DB.connect_db()


@app.on_event('shutdown')
async def shutdown() -> None:
    await DB.disconnect_db()


@app.exception_handler(Exception)
async def common_exception_handler(request: Request, exception: Exception):
    logger.info(f"Status code {exception.code} Message: {exception.error}")
    return JSONResponse(
        status_code=exception.code,
        content={'details': exception.error}
    )


@app.exception_handler(HTTPException)
async def http_exception(request: Request, exc: HTTPException):
    logger.info(f"Status code {exc.status_code} Message: {exc.detail}")
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
    )


@app.middleware("http")
async def log_requst(request: Request, call_next):
    logger.info("***INFO**")
    logger.info(f"Date time: {time.ctime()}")
    logger.info(f"Start request path={request.url.path} Method {request.method}")
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time)
    formatted_process_time = '{0:.5f}'.format(process_time)
    logger.info(f"Completed_in = {formatted_process_time}s")
    # logger.info(f"Status_code = { response.status_code}")
    return response


app.include_router(message_router)
app.include_router(users_router)
app.include_router(lessons_router)
app.include_router(homework_router)
app.include_router(groups_router)
