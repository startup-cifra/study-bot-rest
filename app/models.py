from datetime import datetime
from pydantic import BaseModel, Field


class Message(BaseModel):
    tg_id: int = Field(None, title='Telegram ID', gt=0)
    chat_id: int = Field(None, title='ID чата', gt=0)
    body: str = Field(None, title='Тело сообщения')
    date: datetime = Field(None, title='Время отправки сообщения')


class UserStudent(BaseModel):
    user_name: str = Field(None, title=' Имя в телеграмме')
    # role : int = Field(None, title='Роль в курсе')
    tg_id: int = Field(None, title='Telegram ID', gt=0)
    name_student: str = Field(None, title='Имя ученика')
    surname: str = Field(None, title='Фамилия ученика')
    course: int = Field(None, title=' курс ')
    faculty: str = Field(None, title='Факультет')


class Lessons(BaseModel):
    owner_id: int
    chat_id: int
    lesson_type: str
    body: str
    date: datetime = Field(None, title='Время отправки сообщения')


class Homework(BaseModel):
    owner_id: int
    name: str
    deadline: datetime = Field(None, title='Время окончания отправ. дз')
    url: str
