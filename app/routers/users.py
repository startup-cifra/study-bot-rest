from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from app.models import UserStudent
from app.utils import format_records
from app.queries.users import add_admin_sql, add_user_sql, get_user_groups, check_role_sql

users_router = APIRouter(tags=["Users"])


# TODO Добавить Админа
@users_router.put('/user/admin')
async def add_admin(name: str) -> JSONResponse:
    await add_admin_sql(name)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Executed',
    })

@users_router.get('/user/groups')
async def get_user_groups(tg_id: int = Query(None, title='Telegram ID',gt=0)):
    groups = await user_queries.get_user_groups(tg_id)
    groups = format_records(groups)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'groups': groups
    })    

@users_router.post('/user')
async def add_user(student: UserStudent) -> JSONResponse:
    await add_user_sql(student)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Executed',
    })


@users_router.get('/user/check')
async def check_role(name: str) -> JSONResponse:
    role = await check_role_sql(name)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'Role_users': role,
    })

