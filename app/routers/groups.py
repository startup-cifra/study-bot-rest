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


@groups_router.get('/user/{tg_id}/group',
                   response_model=list[models.GroupOut],
                   status_code=status.HTTP_200_OK)
async def get_user_groups(tg_id: int = Path(..., title='Telegram ID', gt=0)):
    groups = await group_queries.get_user_groups(tg_id)
    groups = format_records(groups, models.GroupOut)
    return groups
