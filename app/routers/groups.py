from fastapi import APIRouter, status
from app import models
from app.queries.groups import add_admin_in_group, add_user_group, create_group

groups_router = APIRouter(tags=["Groups"])


@groups_router.post('/user/groups', response_model=models.SuccessfulResponse, status_code=status.HTTP_201_CREATED)
async def add_group_user(tg_id: int, chat_id: int) -> models.SuccessfulResponse:
    await add_user_group(tg_id, chat_id)
    return models.SuccessfulResponse()


@groups_router.post('/group', response_model=models.SuccessfulResponse)
async def add_group(chat_id: int, name: str) -> models.SuccessfulResponse:
    await create_group(chat_id, name)
    return models.SuccessfulResponse()


@groups_router.put('/user/groups', response_model=models.SuccessfulResponse)
async def add_admin(tg_id: int, chat_id: int) -> models.SuccessfulResponse:
    await add_admin_in_group(tg_id, chat_id)
    return models.SuccessfulResponse()
