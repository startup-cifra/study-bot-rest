from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from app.utils import format_records
import app.queries.users as user_queries

users_router = APIRouter(tags=["Users"])


# TODO Добавить Админа
@users_router.post('/user')
async def add_admin(name: str) -> JSONResponse:
    user_queries.add_admin_sql(name)
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
