from datetime import datetime

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

import app.queries.message as message_queries
from app.models import Message
from app.utils import format_records

message_router = APIRouter(tags=["Messages"])

@message_router.post('/message')
async def add_message(message: Message):
    await message_queries.add_new_message(message.tg_id, message.chat_id, message.body, message.date)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        'details': 'Executed'
    })

@message_router.get('/message/group')
async def get_group_messages(chat_id: int = Query(None, title='ID чата',gt=0),
                             start_date: datetime = Query(None, title='Начальная дата поиска'),
                             end_date: datetime = Query(None, title='Конечная дата поиска')):
    messages = await message_queries.get_group_messages(chat_id,start_date,end_date)
    messages = format_records(messages)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'messages': messages
    })

@message_router.get('/message/group/user')
async def get_group_messages_by_user(tg_id: int = Query(None, title='Telegram ID',gt=0),
                                     chat_id: int = Query(None, title='ID чата',gt=0),
                                     start_date: datetime = Query(None, title='Начальная дата поиска'),
                                     end_date: datetime = Query(None, title='Конечная дата поиска')):
    messages = await message_queries.get_group_messages_by_user(tg_id,chat_id,start_date,end_date)
    messages = format_records(messages)
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'messages':messages
    })

@message_router.get('/message/count/group')
async def count_group_messages(chat_id: int = Query(None, title='ID чата',gt=0),
                             start_date: datetime = Query(None, title='Начальная дата поиска'),
                             end_date: datetime = Query(None, title='Конечная дата поиска')):
    number = await message_queries.count_group_messages(chat_id,start_date,end_date)
    return JSONResponse(status_code=status.HTTP_200_OK, content=number)

@message_router.get('/message/count/group/user')
async def get_group_messages_by_user(tg_id: int = Query(None, title='Telegram ID',gt=0),
                                     chat_id: int = Query(None, title='ID чата',gt=0),
                                     start_date: datetime = Query(None, title='Начальная дата поиска'),
                                     end_date: datetime = Query(None, title='Конечная дата поиска')):
    number = await message_queries.count_group_messages_by_user(tg_id,chat_id,start_date,end_date)
    return JSONResponse(status_code=status.HTTP_200_OK, content=number)
