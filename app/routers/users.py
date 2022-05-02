from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app import models
from app.queries.users import add_admin_sql, add_user_sql, check_role_sql

users_router = APIRouter(tags=["Users"])


# TODO Добавить Админа
@users_router.put('/user/admin', response_model=models.SuccessfulResponse, status_code=status.HTTP_200_OK)
async def add_admin(name: str) -> models.SuccessfulResponse:
    await add_admin_sql(name)
    return models.SuccessfulResponse()


@users_router.post('/user', response_model=models.SuccessfulResponse, status_code=status.HTTP_200_OK)
async def add_user(student: models.UserStudent) -> models.SuccessfulResponse:
    await add_user_sql(student)
    return models.SuccessfulResponse()


@users_router.get('/user/check')
async def check_role(name: str) -> JSONResponse:
    role = await check_role_sql(name)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'Role_users': role,
    })
