from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from app import models
from app.utils import format_records
from app.queries.users import add_user_sql, get_user_groups, check_role_sql

users_router = APIRouter(tags=["Users"])


@users_router.post('/user', response_model=models.SuccessfulResponse, status_code=status.HTTP_201_CREATED)
async def add_user(student: models.UserStudent) -> models.SuccessfulResponse:
    await add_user_sql(student)
    return models.SuccessfulResponse()


@users_router.get('/user/check')
async def check_role(tg_id: int, chat_id: int) -> JSONResponse:
    role = await check_role_sql(tg_id, chat_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'role_users': role,
    })
