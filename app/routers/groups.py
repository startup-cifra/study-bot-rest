from fastapi import APIRouter, Path, status

import app.queries.groups as group_queries
from app import models
from app.utils import format_records

groups_router = APIRouter(tags=["Groups"])


@groups_router.post('/group',
                    response_model=models.SuccessfulResponse,
                    status_code=status.HTTP_201_CREATED)
async def add_group(group: models.Group):
    await group_queries.add_group(group.chat_id, group.name)
    return models.SuccessfulResponse()


@groups_router.post('/user/{tg_id}/group',
                    response_model=models.SuccessfulResponse,
                    status_code=status.HTTP_201_CREATED)
async def add_user_to_group(group: models.GroupIn, tg_id: int = Path(..., title='Telegram ID', gt=0)):
    await group_queries.add_user_to_group(tg_id, group.chat_id, group.role)
    return models.SuccessfulResponse()


@groups_router.delete('/user/{tg_id}/group',
                      response_model=models.SuccessfulResponse)
async def remove_user_from_group(group: models.GroupOut, tg_id: int = Path(..., title='Telegram ID', gt=0)):
    await group_queries.remove_user_from_group(tg_id, group.chat_id)
    return models.SuccessfulResponse()


@groups_router.get('/user/{tg_id}/group',
                   response_model=list[models.GroupOut])
async def get_user_groups(tg_id: int = Path(..., title='Telegram ID', gt=0)):
    groups = await group_queries.get_user_groups(tg_id)
    groups = format_records(groups, models.GroupOut)
    return groups

@groups_router.get('/group/users', response_model=list[models.UserStudent])
async def get_users_in_group(chat_id: int):
    users = await group_queries.get_users_in_group(chat_id)
    return users
