from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from app.exceptions import CommonException, InternalServerError
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

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

app = FastAPI(title='Telegram Bot')


@app.on_event('startup')
async def startup() -> None:
    await DB.connect_db()


@app.on_event('shutdown')
async def shutdown() -> None:
    await DB.disconnect_db()


@app.middleware("http")
async def log_requst(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time)
    formatted_process_time = '{0:.5f}'.format(process_time)
    logger.info(f"""***INFO*** Date time: {time.ctime()}  path={request.url.path} Method {request.method}
                Completed_in = {formatted_process_time}s""")
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"***ERROR*** Status code 422 Message: {str(exc)}")
    return JSONResponse(
        status_code=422,
        content={'details': exc.errors()}
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception(request, exc):
    logger.error(f"***ERROR*** Status code {exc.status_code} Message: {exc.detail}")
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def common_exception_handler(request: Request, exception: Exception):
    error = InternalServerError(debug=str(exception))
    logger.error(f"***ERROR*** Status code {error.status_code} Message: {error.message}")
    return JSONResponse(
        status_code=error.status_code,
        content=error.to_json()
    )


@app.exception_handler(CommonException)
async def unicorn_api_exception_handler(request: Request, exc: CommonException):
    logger.error(f"***ERROR*** Status code {exc.code} Message: {exc.error}")
    return JSONResponse(
        status_code=exc.code,
        content=exc.error
    )

app.include_router(message_router)
app.include_router(users_router)
app.include_router(lessons_router)
app.include_router(homework_router)
app.include_router(groups_router)
