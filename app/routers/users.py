from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.queries.users import add_admin_sql

users_router = APIRouter(tags=["Users"])


# TODO Добавить Админа
@users_router.post('/user')
async def add_admin(name: str) -> JSONResponse:
    add_admin_sql(name)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'details': 'Executed',
    })