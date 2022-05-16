from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Roles(str, Enum):
    STUDENT: str = 'student'
    TUTOR: str = 'tutor'


class SuccessfulResponse(BaseModel):
    details: str = Field('Выполнено', title='Статус операции')


class Message(BaseModel):
    tg_id: int = Field(..., title='Telegram ID', gt=0)
    chat_id: int = Field(..., title='ID чата')
    body: str = Field(..., title='Тело сообщения')
    date: datetime = Field(..., title='Время отправки сообщения')


class MessageOut(BaseModel):
    tg_id: int = Field(None, title='Telegram ID', gt=0)
    chat_id: int = Field(None, title='ID чата')
    body: str = Field(..., title='Тело сообщения')
    date: datetime = Field(..., title='Время отправки сообщения')


class MessageCountOut(BaseModel):
    count: int = Field(None, title='Кол-во сообщений')


class Group(BaseModel):
    name: str = Field(..., title='Имя группы')
    chat_id: int = Field(..., title='ID чата')


class GroupIn(BaseModel):
    chat_id: int = Field(..., title='ID чата')
    role: Roles = Field(..., title='Роль')


class GroupOut(BaseModel):
    name: str = Field(None, title='Имя группы')
    role: str = Field(None, title='Роль')
    chat_id: int = Field(None, title='ID чата')


class AttendanceOut(BaseModel):
    attendance: int = Field(..., title='Посещаемость')


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


class LessonsOutUsers(BaseModel):
    body: str = Field(None, title='Тема урока')
    data: datetime = Field(None, title='Дата')
    lesson_type: str = Field(None, title='Тип урока')
    owner_id: str = Field(None, title=' tutor_id')


class LessonsOut(BaseModel):
    body: str = Field(None, title='Тема урока')
    attendance: int = Field(None, title='Посещаемость')
    data: datetime = Field(None, title='Дата')
    lesson_type: str = Field(None, title='Тип урока')


class Homework(BaseModel):
    owner_id: int = Field(None, title='ID создателя', gt=0)
    name: str = Field(None, title='Имя домашней работы')
    deadline: datetime = Field(None, title='Время окончания отправ. дз')
    url: str = Field(None, title='Ссылка на материалы')
    chat_id: int = Field(None, title='ID группы')


class HomeworkMark(BaseModel):
    tg_id: int = Field(..., title='Telegram ID', gt=0)
    hw_id: int = Field(..., title='Идентификатор дз', gt=0)
    mark: int = Field(..., title='Оценка за дз')


class HomeworkOut(BaseModel):
    hw_id: int = Field(None, title='Идентификатор дз')
    name: str = Field(None, title='Имя домашней работы')
    deadline: datetime = Field(None, title='Время окончания отправ. дз')
    url: str = Field(None, title='Ссылка на материалы')


class СheckHomeworkOut(BaseModel):
    hw_id: int = Field(None, title='Идентификатор дз')
    owner_id: int = Field(None, title='ID создателя')
    name: str = Field(None, title='Имя домашней работы')
    deadline: datetime = Field(None, title='Время окончания отправ. дз')
    url: str = Field(None, title='Ссылка на материалы')
    mark: int = Field(None, title='Оценка дз')
