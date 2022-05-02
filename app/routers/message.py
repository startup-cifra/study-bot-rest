from datetime import datetime

from fastapi import APIRouter, Query, status

import app.queries.message as message_queries
from app import models
from app.utils import format_records

message_router = APIRouter(tags=["Messages"])


@message_router.post('/message', response_model=models.SuccessfulResponse, status_code=status.HTTP_201_CREATED)
async def add_message(message: models.Message):
    await message_queries.add_new_message(message.tg_id, message.chat_id, message.body, message.date)
    return models.SuccessfulResponse()


@message_router.get('/message/group', response_model=list[models.MessageOut], status_code=status.HTTP_200_OK)
async def get_group_messages(chat_id: int = Query(None, title='ID чата', gt=0),
                             start_date: datetime = Query(None, title='Начальная дата поиска'),
                             end_date: datetime = Query(None, title='Конечная дата поиска')):
    messages = await message_queries.get_group_messages(chat_id, start_date, end_date)
    messages = format_records(messages, models.MessageOut)
    return messages


@message_router.get('/message/group/user', response_model=list[models.MessageOut], status_code=status.HTTP_200_OK)
async def get_group_messages_by_user(tg_id: int = Query(None, title='Telegram ID', gt=0),
                                     chat_id: int = Query(None, title='ID чата', gt=0),
                                     start_date: datetime = Query(None, title='Начальная дата поиска'),
                                     end_date: datetime = Query(None, title='Конечная дата поиска')):
    messages = await message_queries.get_group_messages_by_user(tg_id, chat_id, start_date, end_date)
    messages = format_records(messages, models.MessageOut)
    return messages

@message_router.get('/message/group/count', response_model=models.MessageCountOut, status_code=status.HTTP_200_OK)
async def count_group_messages(chat_id: int = Query(None,title="ID чата",gt=0),
                               start_date: datetime = Query(None, title='Начальная дата поиска'),
                               end_date: datetime = Query(None, title='Конечная дата поиска')):
    number = await message_queries.count_group_messages(chat_id, start_date, end_date)
    return models.MessageCountOut(count=number)

@message_router.get('/message/group/user/count',response_model=models.MessageCountOut, status_code=status.HTTP_200_OK)
async def count_group_messages_by_user(tg_id: int = Query(None, title='Telegram ID',gt=0),
                                     chat_id: int = Query(None, title='ID чата',gt=0),
                                     start_date: datetime = Query(None, title='Начальная дата поиска'),
                                     end_date: datetime = Query(None, title='Конечная дата поиска')):
    number = await message_queries.count_group_messages_by_user(tg_id, chat_id, start_date, end_date)
    return models.MessageCountOut(count=number)
