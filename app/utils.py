from datetime import datetime
from asyncpg import Record

def format_records(raw_records: list[Record]) -> list[dict]:
    if not raw_records:
        return []
    result = list(map(dict,raw_records))
    for i in range(len(result)):
        for key in result[i].keys():
            if isinstance(result[i][key], datetime):
                result[i][key] = str(result[i][key])
    return result
