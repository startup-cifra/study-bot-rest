from datetime import datetime
from pydantic import BaseModel, Field

class SuccessfulResponse(BaseModel):
    details: str = Field('Выполнено', title='Статус операции')

class Message(BaseModel):
    tg_id: int = Field(..., title='Telegram ID',gt=0)
    chat_id: int = Field(...,title='ID чата',gt=0)
    body: str = Field(..., title='Тело сообщения')
    date: datetime = Field(..., title='Время отправки сообщения')

class MessageOut(BaseModel):
    tg_id: int = Field(None, title='Telegram ID')
    chat_id: int = Field(None, title='ID чата')
    body: str = Field(..., title='Тело сообщения')
    date: datetime = Field(..., title='Время отправки сообщения')

class MessageCountOut(BaseModel):
    count: int = Field(None,title='Кол-во сообщений')

class GroupOut(BaseModel):
    name: str = Field(None,title='Имя группы')
    chat_id: int = Field(None, title='ID чата')

class AttendanceOut(BaseModel):
    attendance: int = Field(...,title='Посещаемость')

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

class LessonsOut(BaseModel):
    body: str = Field(None, title='Тема урока')
    attendance: int = Field(None, title='Посещаемость')
    data: str = Field(None, title='Дата')
    lesson_type: str = Field(None, title='Тип урока')

class Homework(BaseModel):
    owner_id: int = Field(None, title='ID создателя')
    name: str = Field(None, title='Имя домашней работы')
    deadline: datetime = Field(None, title='Время окончания отправ. дз')
    url: str = Field(None,title='Ссылка на материалы')
