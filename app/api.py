import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.migrations.db import DB
from app.routers.message import message_router
from app.routers.users import users_router
from app.exceptions import CommonException, InternalServerError

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
    del request
    logger.error(exception.error)
    if isinstance(exception,InternalServerError):
        return JSONResponse(
            status_code=exception.code,
            content={'details':'Internal server error'}
        )        
    return JSONResponse(
        status_code=exception.code,
        content={'details': exception.error}
    )
    

app.include_router(message_router)
app.include_router(users_router)
