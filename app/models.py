from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    tg_id: int = Field(None, title='Telegram ID',gt=0)
    chat_id: int = Field(None,title='ID чата',gt=0)
    body: str = Field(None, title='Тело сообщения')
    date: datetime = Field(None, title='Время отправки сообщения')
    
