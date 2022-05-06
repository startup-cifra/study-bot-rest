from typing import Type
from asyncpg import Record
from app.models import BaseModel


def format_records(raw_records: list[Record], model: Type[BaseModel]) -> list[BaseModel]:
    if not raw_records:
        return []
    return list(map(lambda x: model(**x), raw_records))
