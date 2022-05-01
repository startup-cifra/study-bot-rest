from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from app import models
from app.utils import format_records
from app.queries.users import add_admin_sql, add_user_sql, get_user_groups, check_role_sql

users_router = APIRouter(tags=["Users"])


# TODO Добавить Админа
@users_router.put('/user/admin', response_model=models.SuccessfulResponse, status_code=status.HTTP_200_OK)
async def add_admin(name: str) -> models.SuccessfulResponse:
    await add_admin_sql(name)
    return models.SuccessfulResponse()

@users_router.get('/user/groups', response_model=list[models.GroupOut], status_code=status.HTTP_200_OK)
async def get_groups(tg_id: int = Query(None, title='Telegram ID',gt=0)) -> list[models.GroupOut]:
    groups = await get_user_groups(tg_id)
    groups = format_records(groups,models.GroupOut)
    return groups

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
